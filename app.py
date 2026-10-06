from vision import analyze_clothing_image
import streamlit as st
from pathlib import Path

from database import (
    create_user,
    get_user,
    add_wardrobe_item,
    get_wardrobe_items,
    delete_wardrobe_item,
)

st.set_page_config(
    page_title="StyleMind",
    page_icon="👗",
    layout="wide"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ---------- Custom styling ----------
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.15rem;
        opacity: 0.75;
        margin-bottom: 2rem;
    }

    .card {
        padding: 1.2rem;
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 16px;
        min-height: 120px;
        background: rgba(128,128,128,0.04);
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("👗 StyleMind")
st.sidebar.caption("AI Outfit & Personal Style Agent")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👚 My Wardrobe",
        "✨ Generate Outfit",
        "🧠 My Style",
        "💬 AI Stylist",
        "📅 Outfit Planner",
        "📜 Outfit History",
    ],
)

# ---------- Load current user ----------
user = get_user()

# ---------- Dashboard ----------
if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">👗 StyleMind</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI Outfit & Personal Style Knowledge Agent</div>',
        unsafe_allow_html=True
    )

    if user:
        st.success(f"Welcome back, {user[1]}! 👋")
        wardrobe_items = get_wardrobe_items(user[0])
    else:
        wardrobe_items = []
        st.write(
            "Your personal fashion assistant for understanding your wardrobe, "
            "style preferences, occasions, and outfit combinations."
        )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f'<div class="card"><h3>👚 Wardrobe</h3>'
            f'<p>{len(wardrobe_items)} clothing items</p></div>',
            unsafe_allow_html=True
        )

    with col2:
        favorite = user[3] if user and user[3] else "Not configured"

        st.markdown(
            f'<div class="card"><h3>🧠 Personal Style</h3>'
            f'<p>{favorite}</p></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="card"><h3>✨ Outfits</h3>'
            '<p>0 recommendations</p></div>',
            unsafe_allow_html=True
        )

    st.markdown("### ✨ Today's Recommendation")

    st.info(
        "The AI recommendation engine will be connected in later stages."
    )

    st.markdown("### 🚀 What StyleMind will do")

    st.write(
        "• Understand your clothes\n"
        "• Remember your style preferences\n"
        "• Retrieve useful fashion knowledge\n"
        "• Generate outfits for different occasions\n"
        "• Learn from your feedback"
    )


# ---------- Wardrobe ----------
elif page == "👚 My Wardrobe":

    st.title("👚 My Wardrobe")

    st.write(
        "Add your clothes to your digital wardrobe. "
        "AI image analysis will be added in Stage 4."
    )

    if not user:
        st.warning(
            "Please create your style profile first in 🧠 My Style."
        )
        st.stop()

    st.subheader("➕ Add Clothing Item")

    uploaded = st.file_uploader(
        "Upload a clothing image",
        type=["png", "jpg", "jpeg"],
        help="Upload a clear photo of one clothing item."
    )
    if uploaded:

        st.image(
        uploaded,
        caption="Uploaded clothing image",
        width=250
    )

    if st.button(
        "🤖 Analyze Clothing with AI",
        use_container_width=True
    ):

        temp_path = UPLOAD_DIR / f"analysis_{uploaded.name}"

        temp_path.write_bytes(
            uploaded.getbuffer()
        )

        try:

            with st.spinner("AI is analyzing the clothing..."):

                analysis = analyze_clothing_image(
                    str(temp_path)
                )

            st.session_state["clothing_analysis"] = analysis

            st.success("AI analysis completed! ✅")

        except Exception as error:

            st.error(
                "AI analysis failed."
            )

            st.code(str(error))
    if "clothing_analysis" in st.session_state:

        analysis = st.session_state["clothing_analysis"]

        st.subheader("🤖 AI Clothing Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Clothing Type:** "
                f"{analysis['clothing_type']}"
            )

            st.write(
                f"**Color:** "
                f"{analysis['color']}"
            )

            st.write(
                f"**Pattern:** "
                f"{analysis['pattern']}"
            )

            st.write(
                f"**Material:** "
                f"{analysis['material']}"
            )

            st.write(
                f"**Style:** "
                f"{analysis['style']}"
            )

        with col2:

            st.write(
                f"**Season:** "
                f"{analysis['season']}"
            )

            st.write(
                f"**Formality:** "
                f"{analysis['formality']}"
            )

            st.write(
                "**Matching Colors:** "
                + ", ".join(analysis["matching_colors"])
            )

            st.write(
                f"**Confidence:** "
                f"{analysis['confidence']}"
            )

        st.info(
            f"AI notes: {analysis['notes']}"
        )

    with st.form("wardrobe_form"):

        item_name = st.text_input(
            "Item Name",
            placeholder="Example: White Shirt"
        )

        clothing_type = st.selectbox(
            "Clothing Type",
            [
                "T-Shirt",
                "Shirt",
                "Jeans",
                "Trousers",
                "Dress",
                "Skirt",
                "Shorts",
                "Jacket",
                "Hoodie",
                "Sweater",
                "Shoes",
                "Other"
            ]
        )

        color = st.selectbox(
            "Color",
            [
                "Black",
                "White",
                "Blue",
                "Red",
                "Green",
                "Yellow",
                "Pink",
                "Brown",
                "Beige",
                "Grey",
                "Other"
            ]
        )

        pattern = st.selectbox(
            "Pattern",
            [
                "Plain",
                "Striped",
                "Checked",
                "Printed",
                "Floral",
                "Graphic",
                "Other"
            ]
        )

        material = st.text_input(
            "Material",
            placeholder="Example: Cotton"
        )

        style = st.selectbox(
            "Style",
            [
                "Casual",
                "Formal",
                "Minimal",
                "Streetwear",
                "Traditional",
                "Sporty",
                "Other"
            ]
        )

        season = st.selectbox(
            "Season",
            [
                "All-season",
                "Summer",
                "Winter",
                "Monsoon",
                "Spring",
                "Autumn"
            ]
        )

        formality = st.selectbox(
            "Formality",
            [
                "Casual",
                "Smart Casual",
                "Formal"
            ]
        )

        submitted = st.form_submit_button(
            "💾 Add to Wardrobe",
            use_container_width=True
        )

    if submitted:

        if not item_name.strip():
            st.error("Please enter an item name.")

        elif not uploaded:
            st.error("Please upload an image of the clothing item.")

        else:
            # Create a unique filename using the database user and item name.
            safe_name = "".join(
                character if character.isalnum() else "_"
                for character in item_name
            )

            file_path = UPLOAD_DIR / (
                f"{user[0]}_{safe_name}_{uploaded.name}"
            )

            file_path.write_bytes(uploaded.getbuffer())

            item_id = add_wardrobe_item(
                user_id=user[0],
                name=item_name.strip(),
                clothing_type=clothing_type,
                color=color,
                pattern=pattern,
                material=material.strip(),
                style=style,
                season=season,
                formality=formality,
                image_path=str(file_path)
            )

            st.success(
                f"✅ {item_name} was added to your wardrobe! "
                f"Item ID: {item_id}"
            )

    st.divider()

    st.subheader("👗 Your Wardrobe")

    items = get_wardrobe_items(user[0])

    if not items:
        st.info(
            "Your wardrobe is empty. Add your first clothing item above."
        )

    else:
        for item in items:

            (
                item_id,
                name,
                clothing_type,
                color,
                pattern,
                material,
                style,
                season,
                formality,
                image_path,
                created_at
            ) = item

            col1, col2 = st.columns([1, 2])

            with col1:
                if Path(image_path).exists():
                    st.image(
                        image_path,
                        caption=name,
                        width=220
                    )

            with col2:
                st.subheader(name)

                st.write(f"**Type:** {clothing_type}")
                st.write(f"**Color:** {color}")
                st.write(f"**Pattern:** {pattern}")
                st.write(
                    f"**Material:** {material if material else 'Not specified'}"
                )
                st.write(f"**Style:** {style}")
                st.write(f"**Season:** {season}")
                st.write(f"**Formality:** {formality}")

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{item_id}"
                ):
                    delete_wardrobe_item(item_id)
                    st.rerun()

            st.divider()


# ---------- Generate Outfit ----------
elif page == "✨ Generate Outfit":

    st.title("✨ Generate Outfit")

    st.write(
        "Choose an occasion and StyleMind will eventually build "
        "an outfit from your wardrobe."
    )

    occasion = st.selectbox(
        "Occasion",
        [
            "College",
            "Interview",
            "Presentation",
            "Party",
            "Date",
            "Wedding",
            "Travel",
            "Casual Outing",
            "Festival",
        ],
    )

    if st.button(
        "✨ Generate Outfit",
        use_container_width=True
    ):
        st.info(
            f"AI outfit generation for **{occasion}** "
            "will be connected in a later stage."
        )


# ---------- My Style ----------
elif page == "🧠 My Style":

    st.title("🧠 My Style")

    st.write(
        "Tell StyleMind about your personal fashion preferences. "
        "These preferences are saved in SQLite."
    )

    existing_name = user[1] if user else ""

    name = st.text_input(
        "Your Name",
        value=existing_name
    )

    colors = st.multiselect(
        "Preferred Colors",
        [
            "Black",
            "White",
            "Blue",
            "Red",
            "Green",
            "Yellow",
            "Pink",
            "Brown",
            "Beige",
            "Grey"
        ]
    )

    styles = st.multiselect(
        "Favorite Styles",
        [
            "Casual",
            "Formal",
            "Minimal",
            "Streetwear",
            "Traditional",
            "Sporty"
        ]
    )

    dislikes = st.multiselect(
        "Styles or colors you dislike",
        [
            "Bright Colors",
            "Formal",
            "Streetwear",
            "Traditional",
            "Oversized",
            "Skinny Fit"
        ]
    )

    if st.button(
        "💾 Save Style Preferences",
        use_container_width=True
    ):

        if not name.strip():
            st.error("Please enter your name.")

        else:
            user_id = create_user(
                name,
                colors,
                styles,
                dislikes
            )

            st.success(
                f"Profile saved successfully! User ID: {user_id}"
            )

            st.write("Name:", name)
            st.write(
                "Preferred colors:",
                ", ".join(colors) if colors else "Not selected"
            )
            st.write(
                "Favorite styles:",
                ", ".join(styles) if styles else "Not selected"
            )
            st.write(
                "Avoid:",
                ", ".join(dislikes) if dislikes else "Not selected"
            )


# ---------- AI Stylist ----------
elif page == "💬 AI Stylist":

    st.title("💬 AI Stylist")

    st.write(
        "Chat with your personal fashion assistant."
    )

    question = st.chat_input(
        "Ask: What should I wear for college?"
    )

    if question:

        st.chat_message("user").write(question)

        st.chat_message("assistant").write(
            "The AI model is not connected yet. "
            "Later this chat will use your wardrobe, "
            "preferences, RAG knowledge, and outfit history."
        )


# ---------- Outfit Planner ----------
elif page == "📅 Outfit Planner":

    st.title("📅 Outfit Planner")

    st.write(
        "Plan outfits for upcoming days."
    )

    day = st.date_input("Choose a date")

    occasion = st.selectbox(
        "Choose an occasion",
        [
            "College",
            "Presentation",
            "Party",
            "Travel",
            "Casual",
            "Other"
        ]
    )

    if st.button(
        "➕ Add to Planner",
        use_container_width=True
    ):

        st.success(
            f"Planner entry created for "
            f"{day.strftime('%d %b %Y')} — {occasion}."
        )


# ---------- Outfit History ----------
elif page == "📜 Outfit History":

    st.title("📜 Outfit History")

    st.write(
        "Your previous AI outfit recommendations "
        "will appear here."
    )

    st.info("No outfit history yet.")
