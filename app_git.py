import streamlit as st
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
import pandas as pd

# ATTENTION user = root mdp = rootpass 

# dico donnees comptes et initialisation

# import df
user_df = pd.read_csv("data/df_login.csv")

# Créate 2 name as index and as colums  
user_df["name_display"] = user_df["name"]


# create dict
user_df = user_df.set_index('name_display')

dict_user = user_df.to_dict('index')

print(dict_user)
donnees_comptes = {
    'usernames': dict_user
}


authenticator = Authenticate(
    donnees_comptes,  
    "cookie name",         
    "cookie key",          
    30,                    
) 

# ---------------------Page AUTHENTIFICATION---------------------


#tabulates pour login et register
if not st.session_state["authentication_status"]:
    login, tab_register = st.tabs(["Connexion", "Créer un compte"])

    with login :
        authenticator.login("main")
#Creation d'un nouvel utilisateur
    with tab_register : 
        try:
            email_of_registered_user, \
            username_of_registered_user, \
            password_of_registered_user = authenticator.register_user("main")
            if email_of_registered_user:
                st.success('User registered successfully')
                new_user = {
                    "name": username_of_registered_user,
                    "password": password_of_registered_user,
                    "email": email_of_registered_user,
                    "failed_login_attemps": 0,
                    "logged_in": False,
                    "role": "utilisateur"
            }
                #ajout dans le csv
                df = pd.read_csv("data/df_login.csv")   
                df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
                df.to_csv("data/df_login.csv", index=False)
                
#affiche l'erreur (captcha non coché, champs non remplis, etc)               
        except Exception as e:
            st.error(e)
# Gestion des etats de l'auth

elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplie')



# ---------------------SIDEBAR ---------------------

if st.session_state["authentication_status"]:
    with st.sidebar:
        # Bouton de déconnexion
        add_deco = authenticator.logout("Déconnexion")
        st.write(f"Bienvenu : {st.session_state['name']}")
        # Option menu
        selection = option_menu(
            menu_title=None,
            options = ["Accueil", "Les Photos de mon chat"]
        )


# -------------------------AFFICHAGE DES PAGES -------------------------

if st.session_state["authentication_status"]:
    if selection == "Accueil":
        st.title("Bienvenu sur ma page")
        st.image("https://c7.alamy.com/compfr/2db9g0g/enfants-mains-construire-colore-allemand-word-applaus-signifie-applause-arriere-plan-isole-blanc-2db9g0g.jpg")
        
    elif selection == "Les Photos de mon chat":
        st.title("Bienvenu dans l'album de mon chat")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://www.assuropoil.fr/wp-content/uploads/2023/07/avoir-un-chat-sante.jpg")     
        with col2:
            st.image("https://www.solidarite-peuple-animal.com/data/document/1/183.800.jpg?1764671364")
        with col3:  
            st.image("https://www.la-spa.fr/app/app/uploads/2023/07/prendre-soin_duree-vie-chat.jpg")