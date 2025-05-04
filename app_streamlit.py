import streamlit as st
import pandas as pd
import requests

# === Configuration ===
API_URL = "https://api-credit-scoring-v2.onrender.com"
DATA_PATH = "data_sample/X_test_clean.csv"

st.set_page_config(page_title="Simulation Crédit", page_icon="💳")
st.title("💳 Prédiction de Risque de Crédit")
st.markdown("Choisissez un identifiant client pour simuler une prédiction.")

# === Chargement des identifiants clients ===
@st.cache_data
def load_client_ids():
    try:
        df = pd.read_csv(DATA_PATH)
        if "SK_ID_CURR" in df.columns:
            return df["SK_ID_CURR"].astype(int).tolist()
        else:
            st.error("❌ La colonne SK_ID_CURR est manquante.")
            return []
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {e}")
        return []

client_ids = load_client_ids()

# === Interface utilisateur ===
if not client_ids:
    st.warning("⚠️ Aucun identifiant client disponible.")
else:
    client_id = st.selectbox("🔎 Identifiant client :", client_ids)

    if st.button("Prédire le risque"):
        with st.spinner("⏳ Envoi de la requête à l'API..."):
            try:
                response = requests.get(f"{API_URL}/predict/{client_id}")
                result = response.json()

                if "error" in result:
                    st.error(f"🚫 {result['error']}")
                else:
                    st.success("✅ Prédiction reçue !")
                    st.metric("📉 Probabilité de défaut", f"{result['probability']:.2%}")
                    st.metric("📊 Décision", result["decision"])
                    st.metric("📈 Seuil métier", f"{result['seuil_metier']:.2f}")
                    st.markdown("---")
                    st.json(result)

            except Exception as e:
                st.error(f"❌ Erreur de requête : {e}")
