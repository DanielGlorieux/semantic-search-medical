# Script de compilation LaTeX
# Auteur: ILBOUDO P. Daniel Glorieux

param(
    [string]$File = "rapport_recherche_semantique",
    [switch]$Clean,
    [switch]$Draft,
    [switch]$View
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Compilation Rapport LaTeX" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Nettoyer si demandé
if ($Clean) {
    Write-Host "[1/4] Nettoyage des fichiers auxiliaires..." -ForegroundColor Yellow
    Remove-Item -Path "*.aux", "*.log", "*.out", "*.toc", "*.bcf", "*.run.xml", "*.listing", "*.nlo", "*.synctex.gz" -ErrorAction SilentlyContinue
    Write-Host "      Nettoyage termine!" -ForegroundColor Green
    Write-Host ""
}

# Compilation
Write-Host "[2/4] Compilation PDF (1ere passe)..." -ForegroundColor Yellow

if ($Draft) {
    $output = & pdflatex -interaction=nonstopmode -draftmode "$File.tex" 2>&1
} else {
    $output = & pdflatex -interaction=nonstopmode "$File.tex" 2>&1
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERREUR lors de la compilation!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Dernières lignes du log:" -ForegroundColor Yellow
    Get-Content "$File.log" -Tail 30
    exit 1
} else {
    Write-Host "      Passe 1 OK!" -ForegroundColor Green
}

# Biber si nécessaire
if (Test-Path "$File.bcf") {
    Write-Host "[3/4] Traitement bibliographie..." -ForegroundColor Yellow
    $output = & biber "$File" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      Bibliographie OK!" -ForegroundColor Green
    }
}

# Deuxième passe
Write-Host "[3/4] Compilation PDF (2eme passe)..." -ForegroundColor Yellow
$output = & pdflatex -interaction=nonstopmode "$File.tex" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "      Passe 2 OK!" -ForegroundColor Green
}

# Troisième passe pour TOC
Write-Host "[4/4] Compilation PDF (3eme passe - TOC)..." -ForegroundColor Yellow
$output = & pdflatex -interaction=nonstopmode "$File.tex" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "      Passe 3 OK!" -ForegroundColor Green
} else {
    Write-Host "      AVERTISSEMENT: Erreurs possibles" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Compilation terminee!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Statistiques
if (Test-Path "$File.pdf") {
    $pdfSize = (Get-Item "$File.pdf").Length / 1MB
    Write-Host "Fichier PDF genere: $File.pdf" -ForegroundColor Green
    Write-Host "Taille: $([math]::Round($pdfSize, 2)) MB" -ForegroundColor Green
    
    # Compter les pages (approximatif)
    $logContent = Get-Content "$File.log" -Raw
    if ($logContent -match '\[(\d+)\]') {
        $pages = $Matches[1]
        Write-Host "Pages: $pages" -ForegroundColor Green
    }
    
    Write-Host ""
    
    # Ouvrir si demandé
    if ($View) {
        Write-Host "Ouverture du PDF..." -ForegroundColor Cyan
        Start-Process "$File.pdf"
    }
} else {
    Write-Host "ERREUR: Le fichier PDF n'a pas ete genere!" -ForegroundColor Red
    Write-Host "Consultez le fichier $File.log pour plus de details" -ForegroundColor Yellow
    exit 1
}

# Résumé des warnings/erreurs
Write-Host "Analyse du log:" -ForegroundColor Cyan
$logContent = Get-Content "$File.log" -Raw

$warnings = [regex]::Matches($logContent, "Warning").Count
$errors = [regex]::Matches($logContent, "Error").Count
$overfull = [regex]::Matches($logContent, "Overfull").Count

Write-Host "  - Avertissements: $warnings" -ForegroundColor $(if ($warnings -gt 0) { "Yellow" } else { "Green" })
Write-Host "  - Erreurs: $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Green" })
Write-Host "  - Overfull boxes: $overfull" -ForegroundColor $(if ($overfull -gt 0) { "Yellow" } else { "Green" })

Write-Host ""
Write-Host "Commandes utiles:" -ForegroundColor Cyan
Write-Host "  .\compile_rapport.ps1 -Clean        # Nettoyer avant compilation" -ForegroundColor Gray
Write-Host "  .\compile_rapport.ps1 -View         # Ouvrir le PDF apres" -ForegroundColor Gray
Write-Host "  .\compile_rapport.ps1 -Clean -View  # Tout en un" -ForegroundColor Gray
