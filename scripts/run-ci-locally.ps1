# Script PowerShell pour exécuter le CI/CD localement
# Auteur: Said Ouchrif
# Date: 2025-01-06

Write-Host "🚀 Exécution du CI/CD Pipeline Localement" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0

# ========================================
# 1. Tests Backend
# ========================================
Write-Host "🧪 1/6 - Exécution des tests backend..." -ForegroundColor Yellow
Set-Location "$PSScriptRoot\..\backend"

try {
    $result = pytest tests/ -v --cov=app --cov-report=term --cov-report=html 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Tests réussis!" -ForegroundColor Green
    } else {
        Write-Host "❌ Tests échoués!" -ForegroundColor Red
        $ErrorCount++
    }
} catch {
    Write-Host "❌ Erreur lors de l'exécution des tests: $_" -ForegroundColor Red
    $ErrorCount++
}

Write-Host ""

# ========================================
# 2. Linting - Flake8
# ========================================
Write-Host "🔍 2/6 - Vérification du code (Flake8)..." -ForegroundColor Yellow

try {
    $result = flake8 app/ --count --show-source --statistics 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Linting réussi!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Problèmes de linting détectés" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Flake8 non installé ou erreur: $_" -ForegroundColor Yellow
}

Write-Host ""

# ========================================
# 3. Formatage - Black
# ========================================
Write-Host "🎨 3/6 - Vérification du formatage (Black)..." -ForegroundColor Yellow

try {
    $result = black app/ --check --diff 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Formatage correct!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Formatage à corriger" -ForegroundColor Yellow
        Write-Host "   Exécutez: black app/" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️ Black non installé ou erreur: $_" -ForegroundColor Yellow
}

Write-Host ""

# ========================================
# 4. Imports - isort
# ========================================
Write-Host "📋 4/6 - Vérification des imports (isort)..." -ForegroundColor Yellow

try {
    $result = isort app/ --check-only --diff 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Imports corrects!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Imports à corriger" -ForegroundColor Yellow
        Write-Host "   Exécutez: isort app/" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️ isort non installé ou erreur: $_" -ForegroundColor Yellow
}

Write-Host ""

# ========================================
# 5. Security - Safety
# ========================================
Write-Host "🔐 5/6 - Scan de sécurité (Safety)..." -ForegroundColor Yellow

try {
    $result = safety check -r requirements.txt --ignore 70612 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Aucune vulnérabilité détectée!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Vulnérabilités détectées" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Safety non installé ou erreur: $_" -ForegroundColor Yellow
}

Write-Host ""

# ========================================
# 6. Validation du modèle ML
# ========================================
Write-Host "🤖 6/6 - Validation du modèle ML..." -ForegroundColor Yellow

Set-Location "$PSScriptRoot\.."

try {
    $pythonScript = @"
import joblib
import os

model_path = 'ml/artifacts/model.joblib'

# Check file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f'Model not found: {model_path}')

# Check file size
size_mb = os.path.getsize(model_path) / (1024 * 1024)
print(f'✅ Model size: {size_mb:.2f} MB')

# Load model
model = joblib.load(model_path)
print(f'✅ Model type: {type(model).__name__}')
print(f'✅ Model loaded successfully!')
"@

    $result = python -c $pythonScript 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Modèle ML validé!" -ForegroundColor Green
        Write-Host $result -ForegroundColor Gray
    } else {
        Write-Host "❌ Erreur de validation du modèle!" -ForegroundColor Red
        $ErrorCount++
    }
} catch {
    Write-Host "❌ Erreur lors de la validation: $_" -ForegroundColor Red
    $ErrorCount++
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan

# ========================================
# Résumé
# ========================================
Write-Host ""
Write-Host "📊 RÉSUMÉ DU CI/CD LOCAL" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if ($ErrorCount -eq 0) {
    Write-Host "✅ SUCCÈS - Tous les tests sont passés!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Vous pouvez maintenant:" -ForegroundColor Cyan
    Write-Host "   1. Commit vos changements: git add ." -ForegroundColor White
    Write-Host "   2. Créer un commit: git commit -m 'your message'" -ForegroundColor White
    Write-Host "   3. Push vers GitHub: git push origin main" -ForegroundColor White
    Write-Host ""
    Write-Host "Le workflow GitHub Actions s'exécutera automatiquement! 🎉" -ForegroundColor Green
} else {
    Write-Host "❌ ÉCHEC - $ErrorCount test(s) échoué(s)" -ForegroundColor Red
    Write-Host ""
    Write-Host "⚠️ Veuillez corriger les erreurs avant de push." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📁 Rapport de couverture: backend/htmlcov/index.html" -ForegroundColor Gray
Write-Host ""

# Retour au dossier racine
Set-Location "$PSScriptRoot\.."

# Ouvrir le rapport de couverture (optionnel)
$openReport = Read-Host "Ouvrir le rapport de couverture HTML? (O/N)"
if ($openReport -eq "O" -or $openReport -eq "o") {
    Start-Process "backend/htmlcov/index.html"
}
