import streamlit as st

def render_tier_toggle():
    """
    Render a toggle for selecting between Personal and Corporate tiers.
    
    Returns:
        str: Selected tier ('personal' or 'corporate')
    """
    st.markdown("""
        <style>
        .tier-toggle {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }
        .tier-option {
            padding: 0.5rem 1rem;
            border: 1px solid #A020F0;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s;
        }
        .tier-option.active {
            background-color: #A020F0;
            color: white;
        }
        .tier-option:first-child {
            border-radius: 20px 0 0 20px;
        }
        .tier-option:last-child {
            border-radius: 0 20px 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize tier in session state if not present
    if "selected_tier" not in st.session_state:
        st.session_state["selected_tier"] = "personal"
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        personal_active = "active" if st.session_state["selected_tier"] == "personal" else ""
        if st.button("Personal Tier", key="personal_tier_btn"):
            st.session_state["selected_tier"] = "personal"
            # Reset model selection when tier changes
            if "selected_model" in st.session_state:
                st.session_state.pop("selected_model")
    
    with col2:
        corporate_active = "active" if st.session_state["selected_tier"] == "corporate" else ""
        if st.button("Corporate Tier", key="corporate_tier_btn"):
            st.session_state["selected_tier"] = "corporate"
            # Reset model selection when tier changes
            if "selected_model" in st.session_state:
                st.session_state.pop("selected_model")
    
    # Display current tier with styling
    tier_display = "Personal" if st.session_state["selected_tier"] == "personal" else "Corporate"
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 1rem;'>
            <span style='background-color: #A020F0; color: white; padding: 0.3rem 1rem; border-radius: 10px;'>
                {tier_display} Tier Active
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    return st.session_state["selected_tier"]

def render_model_chooser(models):
    """
    Render a model selection component.
    
    Args:
        models (list): List of available models for the current tier
        
    Returns:
        str: Name of the selected model
    """
    st.markdown("""
        <style>
        .model-chooser {
            margin-bottom: 1rem;
        }
        .model-option {
            padding: 0.8rem;
            border: 1px solid #A020F0;
            border-radius: 10px;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.3s;
        }
        .model-option:hover {
            background-color: rgba(160, 32, 240, 0.1);
        }
        .model-option.active {
            background-color: #A020F0;
            color: white;
        }
        .model-name {
            font-weight: bold;
        }
        .model-description {
            font-size: 0.8rem;
            opacity: 0.8;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("### Available Models")
    
    # Initialize selected model in session state if not present
    if "selected_model" not in st.session_state and models:
        st.session_state["selected_model"] = models[0].name
    
    # Create a radio button for model selection
    model_options = [model.name for model in models]
    model_descriptions = {model.name: model.description for model in models}
    
    selected_model = st.radio(
        "Select a model:",
        model_options,
        index=model_options.index(st.session_state["selected_model"]) if "selected_model" in st.session_state and st.session_state["selected_model"] in model_options else 0,
        key="model_radio"
    )
    
    # Update session state
    st.session_state["selected_model"] = selected_model
    
    # Display current model with styling
    st.markdown(f"""
        <div style='background-color: rgba(160, 32, 240, 0.1); padding: 0.8rem; border-radius: 10px; margin-top: 1rem;'>
            <div style='font-weight: bold;'>Current Model: {selected_model}</div>
            <div style='font-size: 0.8rem;'>{model_descriptions.get(selected_model, "")}</div>
        </div>
    """, unsafe_allow_html=True)
    
    return selected_model

def display_model_info(model):
    """
    Display information about the currently selected model.
    
    Args:
        model (AIModelInterface): The currently selected model
    """
    info = model.get_info()
    
    st.markdown(f"""
        <div style='background-color: rgba(160, 32, 240, 0.05); padding: 1rem; border-radius: 10px; margin-top: 1rem; border-left: 4px solid #A020F0;'>
            <h4 style='margin-top: 0; color: #A020F0;'>Active Model Information</h4>
            <p><strong>Name:</strong> {info['name']}</p>
            <p><strong>Description:</strong> {info['description']}</p>
            <p><strong>Tier:</strong> {info['tier'].capitalize()}</p>
        </div>
    """, unsafe_allow_html=True)
