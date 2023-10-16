import streamlit as st
from frosthavenattckmoddeck import ModDeck

if 'modDeck' not in st.session_state:
    st.session_state['modDeck'] = ModDeck()
modDeck = st.session_state['modDeck']

if 'resultText' not in st.session_state:
    st.session_state['resultText'] = None
resultText = st.session_state['resultText']

classesKeys = list()
classesNames = list()

def activate_perk(id, perk):
    modDeck.activatePerk(id, perk)
    st.session_state['modDeck'] = modDeck

def add_blessing():
    modDeck.blessingAction()
    st.session_state['modDeck'] = modDeck

def add_curse():
    modDeck.curseAction()
    st.session_state['modDeck'] = modDeck

def draw_card():
    global resultText
    st.session_state['resultText'] = modDeck.drawCardAction()

def draw_2_card():
    global resultText
    st.session_state['resultText'] = modDeck.draw2CardAction()

def shuffle():
    modDeck.shuffleAction()
    st.session_state['modDeck'] = modDeck

for key in modDeck.Classes:
    classesKeys.append(key)
    classesNames.append(modDeck.Classes[key]["name"])

option = st.selectbox(
    'Character:',
    classesNames,
    index=None,
    placeholder="Select your character"
)


if option is not None:
    modDeck.selectClass(classesKeys[classesNames.index(option)])
    st.session_state['modDeck'] = modDeck

    with st.expander("Perks", True):
        perks = modDeck.Classes[classesKeys[classesNames.index(option)]]["perks"]

        index = 0
        for perk in perks:
            st.checkbox(modDeck.GeneratePerkText(perk), key=f"perk{index}", on_change=activate_perk,
                                          kwargs={"id": index, "perk": perk})
            index += 1

    col1, col2 = st.columns(2)
    with col1:
        st.button("Draw Card", on_click=draw_card)
        st.button("Draw 2 Cards", on_click=draw_2_card)
    with col2:
        st.button("Shuffle", on_click=shuffle)
        st.button("Bless", on_click=add_blessing)
        st.button("Curse", on_click=add_curse)

if resultText is not None:
    st.text(resultText)
    st.session_state['resultText'] = None