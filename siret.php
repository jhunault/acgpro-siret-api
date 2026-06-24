<?php
header("Content-Type: application/json; charset=utf-8");

$nom = urlencode($_GET["nom"]);
$cp = urlencode($_GET["cp"]);

/* ---------------------------------------------------------
   1) Tentative API Annuaire-Entreprises (DNS souvent KO)
--------------------------------------------------------- */
$url1 = "https://api.annuaire-entreprises.data.gouv.fr/search?q=$nom&code_postal=$cp";

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_TIMEOUT, 5);

$response1 = curl_exec($ch);
$err1 = curl_error($ch);
curl_close($ch);

/* Si Annuaire-Entreprises répond correctement */
if ($response1 !== false && strpos($response1, '"results"') !== false) {
    echo $response1;
    exit;
}

/* ---------------------------------------------------------
   2) BASCULE AUTOMATIQUE ? API SIRENE (INSEE)
   Cette API fonctionne même quand Annuaire-Entreprises est KO
--------------------------------------------------------- */
$url2 = "https://entreprise.data.gouv.fr/api/sirene/v3/etablissements?nom_raison_sociale=$nom&code_postal=$cp";

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url2);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_TIMEOUT, 5);

$response2 = curl_exec($ch);
$err2 = curl_error($ch);
curl_close($ch);

/* Si SIRENE répond */
if ($response2 !== false && strpos($response2, '"etablissements"') !== false) {
    echo $response2;
    exit;
}

/* ---------------------------------------------------------
   3) Si les deux APIs échouent ? message d’erreur détaillé
--------------------------------------------------------- */
echo json_encode([
    "error" => "Aucune API accessible",
    "annuaire_entreprises" => $err1,
    "sirene" => $err2
]);
?>
