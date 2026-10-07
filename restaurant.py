import streamlit as st

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="BiteBill",
    page_icon="🍔",
    layout="wide"
)

# =========================================================
# MENU
# =========================================================

menu = {
    "🍔 Classic Burger": 149,
    "🍕 Margherita Pizza": 249,
    "🍟 French Fries": 99,
    "🌯 Chicken Wrap": 179,
    "🍝 Creamy Pasta": 199,
    "🍗 Chicken Biryani": 229,
    "🥤 Cold Drink": 59,
    "🍨 Ice Cream": 89
}

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f7f7f8;
}

/* Page width */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

/* Header */
.header-box {
    background: linear-gradient(135deg, #111827, #252f3f);
    padding: 25px 30px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.header-title {
    color: #ff7900;
    font-size: 32px;
    font-weight: 700;
}

.header-subtitle {
    color: #d1d5db;
    font-size: 14px;
}

/* Section titles */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
}

/* Orange buttons */
.stButton > button {
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    height: 48px;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ea580c, #c2410c);
    color: white;
}

/* Bill total */
.total-box {
    background: linear-gradient(135deg, #f97316, #ea580c);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    color: white;
    margin-top: 15px;
}

.total-title {
    font-size: 13px;
}

.total-value {
    font-size: 30px;
    font-weight: 700;
}

/* Small text */
.small-text {
    color: #9ca3af;
    font-size: 13px;
}

/* Footer */
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 12px;
    padding: 25px 0;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="header-box">'
    '<div class="header-title">🍔JHANSIBiteBill</div>'
    '<div class="header-subtitle">'
    'Simple • Fast • Professional Restaurant Billing'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# SESSION STATE
# =========================================================

if "show_bill" not in st.session_state:
    st.session_state.show_bill = False

# =========================================================
# MAIN LAYOUT
# =========================================================

menu_col, bill_col = st.columns(
    [1.6, 1],
    gap="large"
)

# =========================================================
# LEFT SIDE - MENU
# =========================================================

with menu_col:

    st.markdown(
        '<div class="section-title">🍽️ Choose Your Items</div>',
        unsafe_allow_html=True
    )

    st.write("")

    selected_items = {}

    # -----------------------------------------------------
    # FOOD ITEMS
    # -----------------------------------------------------

    for item, price in menu.items():

        col1, col2, col3 = st.columns(
            [4, 1, 1]
        )

        with col1:

            selected = st.checkbox(
                item,
                key="check_" + item
            )

        with col2:

            st.write(f"**₹{price}**")

        with col3:

            if selected:

                quantity = st.number_input(
                    "Qty",
                    min_value=1,
                    max_value=20,
                    value=1,
                    step=1,
                    key="qty_" + item,
                    label_visibility="collapsed"
                )

            else:

                quantity = 0

        if selected:

            selected_items[item] = {
                "price": price,
                "quantity": quantity
            }

    # =====================================================
    # SETTINGS
    # =====================================================

    st.write("")
    st.markdown(
        '<div class="section-title">⚙️ Bill Settings</div>',
        unsafe_allow_html=True
    )

    st.write("")

    setting1, setting2 = st.columns(2)

    with setting1:

        tax = st.number_input(
            "Tax (%)",
            min_value=0.0,
            max_value=30.0,
            value=5.0,
            step=1.0
        )

    with setting2:

        discount = st.number_input(
            "Discount (%)",
            min_value=0.0,
            max_value=50.0,
            value=0.0,
            step=1.0
        )

    st.write("")

    # =====================================================
    # GENERATE BILL BUTTON
    # =====================================================

    if st.button(
        "🧾 Generate Bill",
        use_container_width=True
    ):

        if len(selected_items) == 0:

            st.session_state.show_bill = False

            st.warning(
                "Please select at least one food item."
            )

        else:

            st.session_state.show_bill = True


# =========================================================
# RIGHT SIDE - BILL
# =========================================================

with bill_col:

    # =====================================================
    # EMPTY BILL
    # =====================================================

    if not st.session_state.show_bill:

        with st.container(border=True):

            st.subheader("🧾 Your Bill")

            st.caption(
                "Select food items to see your bill"
            )

            st.divider()

            # Empty state
            st.markdown(
                "<div style='text-align:center; font-size:50px;'>🍽️</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                "### Your bill will appear here"
            )

            st.caption(
                "Choose items from the menu and click "
                "**Generate Bill**."
            )

    # =====================================================
    # GENERATED BILL
    # =====================================================

    else:

        # -------------------------------------------------
        # CALCULATIONS
        # -------------------------------------------------

        subtotal = 0

        for item, details in selected_items.items():

            subtotal += (
                details["price"]
                * details["quantity"]
            )

        discount_amount = (
            subtotal * discount / 100
        )

        after_discount = (
            subtotal - discount_amount
        )

        tax_amount = (
            after_discount * tax / 100
        )

        grand_total = (
            after_discount + tax_amount
        )

        # -------------------------------------------------
        # BILL CARD
        # -------------------------------------------------

        with st.container(border=True):

            st.markdown(
                "## 🍴 BITEBILL RESTAURANT"
            )

            st.caption(
                "Your Order Receipt"
            )

            st.divider()

            # -------------------------------------------------
            # ITEMS
            # -------------------------------------------------

            for item, details in selected_items.items():

                price = details["price"]
                quantity = details["quantity"]

                item_total = price * quantity

                item_col, total_col = st.columns(
                    [3, 1]
                )

                with item_col:

                    st.write(
                        f"{item} × {quantity}"
                    )

                with total_col:

                    st.write(
                        f"**₹{item_total:.2f}**"
                    )

            st.divider()

            # -------------------------------------------------
            # SUBTOTAL
            # -------------------------------------------------

            row1, row2 = st.columns(2)

            with row1:
                st.write("Subtotal")

            with row2:
                st.write(
                    f"**₹{subtotal:.2f}**"
                )

            # -------------------------------------------------
            # DISCOUNT
            # -------------------------------------------------

            row1, row2 = st.columns(2)

            with row1:
                st.write(
                    f"Discount ({discount:.0f}%)"
                )

            with row2:
                st.write(
                    f"**- ₹{discount_amount:.2f}**"
                )

            # -------------------------------------------------
            # TAX
            # -------------------------------------------------

            row1, row2 = st.columns(2)

            with row1:
                st.write(
                    f"Tax ({tax:.0f}%)"
                )

            with row2:
                st.write(
                    f"**+ ₹{tax_amount:.2f}**"
                )

            # -------------------------------------------------
            # GRAND TOTAL
            # -------------------------------------------------

            st.markdown(
                f"""
                <div class="total-box">
                    <div class="total-title">
                        GRAND TOTAL
                    </div>
                    <div class="total-value">
                        ₹{grand_total:.2f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            st.success(
                "Bill generated successfully!"
            )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'BiteBill • Restaurant Billing System • '
    'Python + Streamlit'
    '</div>',
    unsafe_allow_html=True
)