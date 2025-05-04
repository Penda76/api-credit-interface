import streamlit as st
import requests

API_URL = "https://api-credit-scoring-v2.onrender.com"

st.set_page_config(page_title="Simulation Crédit", page_icon="💳")
st.title("💳 Prédiction de Risque de Crédit")
st.markdown("Saisissez un identifiant client existant pour simuler une prédiction.")

client_id = st.text_input("🔎 Identifiant client :", value="", max_chars=10)

if st.button("Prédire le risque") and client_id:
    try:
        client_id = int(client_id.strip())
        with st.spinner("⏳ Prédiction en cours..."):
            url = f"{API_URL}/predict/{client_id}"
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

    except ValueError:
        st.error("❌ L'identifiant saisi doit être un nombre entier.")
    except Exception as e:
        st.error(f"Erreur : {e}")
