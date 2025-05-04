import streamlit as st
import pandas as pd
import requests

API_URL = "https://api-credit-scoring-v2.onrender.com"

st.set_page_config(page_title="Simulation Crédit", page_icon="💳")
st.title("💳 Prédiction de Risque de Crédit")
st.markdown("Choisissez un identifiant client pour simuler une prédiction.")

@st.cache_data
def load_ids():
    try:
        df = pd.read_csv("X_test_sample_id.csv")
        if "SK_ID_CURR" in df.columns:
            return df["SK_ID_CURR"].astype(int).tolist()
        else:
            st.error("La colonne SK_ID_CURR est manquante.")
            return []
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return []

client_ids = load_ids()

if not client_ids:
    st.warning("Aucun identifiant client trouvé.")
else:
    selected_id = st.selectbox("🔎 Identifiant client :", client_ids)

    if st.button("Prédire"):
        with st.spinner("⏳ Prédiction en cours..."):
            try:
                url = f"{API_URL}/predict/{selected_id}"
                response = requests.get(url)
                result = response.json()

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("✅ Résultat reçu !")
                    st.metric("Probabilité de défaut", f"{result['probability']:.2%}")
                    st.metric("Décision", result["decision"])
                    st.metric("Seuil métier", f"{result['seuil_metier']:.2f}")
                    st.json(result)

            except Exception as e:
                st.error(f"Erreur : {e}")
