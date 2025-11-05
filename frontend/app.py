# frontend/app.py
import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

# ---------- Config ----------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")
PREDICT_ENDPOINT = f"{API_URL}/predict"
HEALTH_ENDPOINT = f"{API_URL}/health"

st.set_page_config(page_title="Car Price Estimator (MA)", page_icon="🚗", layout="centered")

st.title("🚗 Car Price Estimator (MAD)")
st.caption(f"Backend: {API_URL}")

# ---------- Ping /health ----------
try:
    r = requests.get(HEALTH_ENDPOINT, timeout=5)
    if r.ok and r.json().get("status") == "ok":
        st.success("Backend connecté ✅ (model chargé)")
    else:
        st.warning("Backend accessible mais le modèle n'est pas chargé ⚠️")
except Exception as e:
    st.error(f"Impossible de contacter le backend: {e}")

st.divider()

# ---------- Helpers ----------
def owner_label_to_str(label: str) -> str | None:
    mapping = {
        "Inconnu": None,
        "Premier": "First",
        "Deuxième": "Second",
        "Troisième": "Third",
        "Quatrième ou +": "Fourth & Above"
    }
    return mapping.get(label, None)

def validate_inputs(payload: dict) -> list[str]:
    errors = []
    if payload["year"] < 1990 or payload["year"] > 2026:
        errors.append("L'année doit être entre 1990 et 2026.")
    numeric_nonneg = ["km_driven", "engine_cc", "max_power_bhp"]
    for k in numeric_nonneg:
        if payload[k] is None or payload[k] < 0:
            errors.append(f"{k} doit être ≥ 0.")
    if payload["mileage_mpg"] is not None and payload["mileage_mpg"] < 0:
        errors.append("mileage_mpg doit être ≥ 0.")
    if payload["torque_nm"] is not None and payload["torque_nm"] < 0:
        errors.append("torque_nm doit être ≥ 0.")
    for k in ["company", "model", "fuel", "seller_type", "transmission"]:
        if not payload[k]:
            errors.append(f"{k} ne doit pas être vide.")
    return errors

# ---------- Form ----------
with st.form("car_form", clear_on_submit=False):
    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("Marque (company)", value="Toyota", key="company_input")
        model = st.text_input("Modèle (model)", value="Yaris", key="model_input")
        edition = st.text_input("Édition/finition (edition)", value="1.3", key="edition_input")
        year = st.number_input("Année (year)", min_value=1990, max_value=2026, value=2018, step=1, key="year_input")
        owner_lbl = st.selectbox("Propriétaire (owner)", ["Inconnu", "Premier", "Deuxième", "Troisième", "Quatrième ou +"], index=1, key="owner_select")
        fuel = st.selectbox("Carburant (fuel)", ["Petrol", "Diesel", "CNG", "LPG", "Electric"], index=0, key="fuel_select")

    with col2:
        seller_type = st.selectbox("Type vendeur (seller_type)", ["Individual", "Dealer", "Trustmark Dealer"], index=0, key="seller_select")
        transmission = st.selectbox("Transmission", ["Manual", "Automatic"], index=0, key="transmission_select")
        km_driven = st.number_input("Km parcourus (km_driven)", min_value=0, value=82000, step=1000)
        mileage_mpg = st.number_input("Consommation (mileage_mpg)", min_value=0.0, value=45.0, step=0.5, format="%.1f")
        engine_cc = st.number_input("Cylindrée cc (engine_cc)", min_value=0.0, value=1300.0, step=50.0, format="%.1f")
        max_power_bhp = st.number_input("Puissance bhp (max_power_bhp)", min_value=0.0, value=84.0, step=1.0, format="%.1f")
        torque_nm = st.number_input("Couple Nm (torque_nm)", min_value=0.0, value=120.0, step=1.0, format="%.1f")

    submitted = st.form_submit_button("Estimer le prix (MAD)")

if submitted:
    payload = {
        "company": company.strip(),
        "model": model.strip(),
        "edition": edition.strip() if edition else None,
        "year": int(year),
        "owner": owner_label_to_str(owner_lbl),
        "fuel": fuel,
        "seller_type": seller_type,
        "transmission": transmission,
        "km_driven": float(km_driven),
        "mileage_mpg": float(mileage_mpg) if mileage_mpg is not None else None,
        "engine_cc": float(engine_cc),
        "max_power_bhp": float(max_power_bhp),
        "torque_nm": float(torque_nm) if torque_nm is not None else None
    }

    # Validation côté frontend
    errs = validate_inputs(payload)
    if errs:
        st.error("Veuillez corriger les erreurs suivantes :")
        for e in errs:
            st.write(f"• {e}")
    else:
        with st.spinner("Prédiction en cours..."):
            try:
                resp = requests.post(PREDICT_ENDPOINT, json=payload, timeout=10)
                if resp.ok:
                    data = resp.json()
                    price = data.get("price_mad", None)
                    if price is not None:
                        st.success(f"💰 Prix estimé : **{price:,.0f} MAD**")
                        with st.expander("Voir le JSON envoyé", expanded=False):
                            st.code(json.dumps(payload, indent=2, ensure_ascii=False), language="json")
                    else:
                        st.warning(f"Réponse inattendue du serveur: {data}")
                else:
                    st.error(f"Erreur serveur ({resp.status_code}) : {resp.text}")
            except Exception as ex:
                st.error(f"Échec de la requête : {ex}")
