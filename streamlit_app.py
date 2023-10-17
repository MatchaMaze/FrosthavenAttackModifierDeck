import streamlit as st
from frosthavenattckmoddeck import ModDeck

st.markdown('<style>'
            '[data-testid="stHorizontalBlock"],'
            '[data-testid="stExpander"]'
            '{'
            'border-style: solid;'
            'border-color: rgba(250, 250, 250, 1);'
            'border-radius: 0.5rem;'
            'border-width: 1px;'
            'padding: 5px;'
            '}'
            '</style>', unsafe_allow_html=True)

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

    with st.expander("Special Actions"):
        col1, col2, col3 = st.columns(3)
        col1.button("Bless", on_click=add_blessing)
        col2.button("Curse", on_click=add_curse)
    with st.container():
        col7, col8, col9 = st.columns(3)
        col7.write(f"Deck size: {modDeck.active_deck_size()}")
        col8.write(f"Discard size: {modDeck.discard_deck_size()}")
        col9.write(f"Need shuffle: {'Yes' if modDeck.NeedShuffle else 'No'}")
    with st.container():
        col4, col5, col6 = st.columns(3)
        col4.button("Draw Card", on_click=draw_card)
        col5.button("Draw 2 Cards", on_click=draw_2_card)
        col6.button("Shuffle", on_click=shuffle)

if resultText is not None:
    col10 = st.columns(1)
    col10[0].text(resultText)
    st.session_state['resultText'] = None