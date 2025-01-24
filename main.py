import streamlit as st
import plotly.express as px
import time
import random
import math

def character_checker(password):
    lower = sum(1 for char in password if char.islower())
    upper = sum(1 for char in password if char.isupper())
    number = sum(1 for char in password if char.isdigit())
    symbols = sum(1 for char in password if char in "~`!@#$%^&*()_-+={[}]|:;\"'<,>.?/")

    return lower, upper, number, symbols


def points_calculator(lower, upper, number, symbols, password):
    length = len(password)

    if length < 8:
        length_score = 0
    elif 8 <= length <= 9:
        length_score = 1
    elif 10 <= length <= 11:
        length_score = 2
    elif 12 <= length <= 15:
        length_score = 3
    else:
        length_score = 4

    variety_score = sum(1 for x in [lower, upper, number] if x > 0)

    if symbols >= 4:
        variety_score += 3
    elif symbols >= 2:
        variety_score += 2
    elif symbols > 0:
        variety_score += 1

    repeated_characters = any(password[i] == password[i-1] == password[i-2] == password[i-3] for i in range(3, len(password)))
    repetition_penalty = -1 if repeated_characters else 0

    return length_score + variety_score + repetition_penalty


import os
import math

def load_common_passwords():
    """Loads common passwords from pass1.txt, pass2.txt, pass3.txt"""
    common_passwords = set()
    for filename in ["pass1.txt", "pass2.txt", "pass3.txt"]:
        if os.path.exists(filename):  # Ensure the file exists before reading
            with open(filename, "r", encoding="utf-8") as file:
                common_passwords.update(line.strip() for line in file)
    return common_passwords

COMMON_PASSWORDS = load_common_passwords()

def estimate_cracking_time(password):
    """More realistic password cracking time estimation considering real-world attack methods."""
    
    # 🚨 Common Password Check
    if password.lower() in COMMON_PASSWORDS:
        return "⚠️ Instantly Crackable! (Common Password)"
    
    length = len(password)

    # ✅ 1. **Character Pool Calculation**
    character_pools = {
        "lowercase": 26 if any(c.islower() for c in password) else 0,
        "uppercase": 26 if any(c.isupper() for c in password) else 0,
        "digits": 10 if any(c.isdigit() for c in password) else 0,
        "special": 30 if any(c in "~`!@#$%^&*()_-+={[}]|:;\"'<,>.?/" for c in password) else 0,
    }
    
    # If no valid character set, return instantly weak
    if sum(character_pools.values()) == 0:
        return "Instantly (Too Weak)"

    # **New Complexity Formula:** Multiply dynamically per character
    complexity = sum(filter(None, character_pools.values()))
    total_combinations = complexity ** length

    # ✅ 2. **Attack Speeds (More Realistic)**
    attack_speeds = {
        "Brute-force (Old CPU)": 1e9,    # 1 billion guesses/sec
        "Modern GPU": 1e11,              # 100 billion guesses/sec
        "Advanced AI/Cloud": 1e14        # 100 trillion guesses/sec
    }

    # ✅ 3. **Password Pattern Weakness Factor**
    # If password follows common structure (e.g., 'Pass123'), reduce security
    if any(word in password.lower() for word in ["password", "admin", "123", "qwerty", "letmein"]):
        weakness_factor = 10_000  # If predictable, divide by this factor
    else:
        weakness_factor = 1

    # ✅ 4. **Compute Time for Different Attack Scenarios**
    times = {}
    for attack_type, speed in attack_speeds.items():
        seconds_to_crack = (total_combinations / speed) / weakness_factor
        times[attack_type] = format_cracking_time(seconds_to_crack)

    return times

def format_cracking_time(seconds):
    """Formats the cracking time into a human-readable format."""
    if isinstance(seconds, str):  # If password is in common list
        return seconds

    if seconds < 1:
        return "Instantly (Too Weak)"
    
    time_units = [
        ("seconds", 60), ("minutes", 60), ("hours", 24), 
        ("days", 30.44), ("months", 12), ("years", 100)
    ]
    
    value = seconds
    for unit, factor in time_units:
        if value < factor:
            return f"{math.ceil(value)} {unit}"
        value /= factor
    
    return "Millions of years (Very Strong)"




def show_interactive_graph(lower, upper, number, symbols):
    labels = ['Lowercase', 'Uppercase', 'Numbers', 'Symbols']
    values = [lower, upper, number, symbols]

    fig = px.bar(
        x=labels, 
        y=values, 
        labels={"x": "Character Type", "y": "Count"},
        color=values,
        color_continuous_scale="blues"
    )
    
    fig.update_layout(yaxis=dict(tickmode="linear", dtick=1))
    
    st.plotly_chart(fig, use_container_width=True)

import random
import random

def improve_password(password: str):
    substitutions = {
        'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
    }
    
    def replace_few_chars(pwd):
        """Replaces only 1-2 characters to maintain similarity."""
        pwd_list = list(pwd)
        replace_indices = random.sample(range(len(pwd)), min(2, len(pwd)))  # Pick 1-2 random positions
        for idx in replace_indices:
            if pwd_list[idx].lower() in substitutions:
                pwd_list[idx] = substitutions[pwd_list[idx].lower()]
        return ''.join(pwd_list)

    def capitalize_randomly(pwd):
        """Randomly capitalizes 1-2 letters."""
        pwd_list = list(pwd)
        capitalize_indices = random.sample(range(len(pwd)), min(2, len(pwd)))  # Pick 1-2 random positions
        for idx in capitalize_indices:
            pwd_list[idx] = pwd_list[idx].upper()
        return ''.join(pwd_list)

    def add_single_special_char(pwd):
        """Adds a single special character at the beginning or end (optional)."""
        special_chars = "!@#$%^&*"
        if random.choice([True, False]):  # 50% chance of adding a special char
            return pwd + random.choice(special_chars)
        return pwd

    def generate_variation(pwd):
        """Applies minor modifications to the password."""
        modified = replace_few_chars(pwd)
        modified = capitalize_randomly(modified)
        modified = add_single_special_char(modified)
        return modified

    # Generate 4 slightly improved passwords
    improved_passwords = [generate_variation(password) for _ in range(4)]
    
    return improved_passwords

import plotly.graph_objects as go

import plotly.graph_objects as go
import math

def cracking_time_chart(password):
    # Estimate cracking time
    time_to_crack = estimate_cracking_time(password)

    # Define time scales (logarithmic)
    time_labels = [
        "1 sec", "1 min", "1 hr", "1 day", "1 month", "1 year", "100 years", "Million years"
    ]
    time_values = [
        1, 60, 3600, 86400, 2628000, 31536000, 3153600000, 1e12
    ]

    # Find the closest time range
    closest_index = max(i for i, v in enumerate(time_values) if time_to_crack >= v)

    # Create an empty bar chart with only one active bar
    y_values = [0] * len(time_labels)  # Initialize with 0 height
    y_values[closest_index] = math.log10(time_to_crack + 1)  # Assign only one bar

    # Create the figure
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=time_labels,
        y=y_values,
        marker_color="red" if time_to_crack < 3600 else "green"
    ))

    # Update layout
    fig.update_layout(
        title="Estimated Password Cracking Time (Log Scale)",
        xaxis_title="Time to Crack",
        yaxis_title="Log(Seconds)",
        template="plotly_dark",
        yaxis=dict(
            tickvals=[math.log10(val + 1) for val in time_values], 
            ticktext=time_labels
        )
    )

    # Show the chart
    st.plotly_chart(fig, use_container_width=True)



def simulate_cracking_animation(password):
    placeholder = st.empty()
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

    guessed_password = ["_" for _ in password]

    for i in range(50):  # More iterations for better rolling effect
        time.sleep(0.08)  # Faster transitions for a smoother effect

        for j in range(len(password)):
            if guessed_password[j] != password[j]:  
                guessed_password[j] = random.choice(charset)

        with placeholder.container():
            st.write("🔓 **Cracking Password...**")
            cols = st.columns(len(password))
            for j in range(len(password)):
                with cols[j]:
                    st.markdown(f"<p style='font-size:35px; font-weight:bold; text-align:center;'>{guessed_password[j]}</p>", unsafe_allow_html=True)

    # Smoothly transition to the actual password one letter at a time
    for j in range(len(password)):
        time.sleep(0.15)
        guessed_password[j] = password[j]

        with placeholder.container():
            st.write("🔓 **Cracking Password...**")
            cols = st.columns(len(password))
            for k in range(len(password)):
                with cols[k]:
                    font_size = "35px" if k != j else "40px"  # Slight highlight effect
                    st.markdown(f"<p style='font-size:{font_size}; font-weight:bold; text-align:center;'>{guessed_password[k]}</p>", unsafe_allow_html=True)

    # Final reveal with reduced font and centered text
    time.sleep(0.5)
    with placeholder.container():
        st.write("✅ **Password Cracked!**")
        st.markdown(f"<p style='font-size:25px; font-weight:bold; text-align:center;'>{''.join(guessed_password)}</p>", unsafe_allow_html=True)


    # Final reveal with reduced font and centered text
    time.sleep(0.5)
    with placeholder.container():
        st.write("✅ **Password Cracked!**")
        st.markdown(f"<p style='font-size:100px; font-weight:bold; text-align:center;'>{''.join(guessed_password)}</p>", unsafe_allow_html=True)


st.set_page_config(page_title="Password Strength Checker", layout="wide")

st.title("🔐 Password Strength Checker")
st.write("Enter a password below to check its strength and estimated cracking time.")

password = st.text_input("Enter your password:", type="password")

if password:
    with st.spinner("Simulating password cracking..."):
        simulate_cracking_animation(password)

    lower, upper, number, symbols = character_checker(password)
    score = points_calculator(lower, upper, number, symbols, password)
    cracking_time = estimate_cracking_time(password)
    cracking_times = estimate_cracking_time(password)

    




    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔹 Password Strength Score")
        st.metric(label="Score", value=f"{score}/10")
        strength = min(score / 10, 1.0)  # Convert score to a scale of 0-1
        st.progress(strength)


        if score <= 3:
            st.error("🔴 Your password is very weak! Change it immediately.")
        elif score <= 5:
            st.warning("🟠 Your password is weak! Consider improving it.")
        elif score <= 7:
            st.info("🔵 Your password is decent, but could be stronger.")
        elif score <= 9:
            st.success("🟢 Your password is strong!")
        else:
            st.balloons()
            st.success("💪 Your password is very strong!")

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.subheader("💡 Recommended Strong Password")

        passwords = list(improve_password(password))
        scores = [points_calculator(*character_checker(improve_password(password)[0]), improve_password(password)[0]), points_calculator(*character_checker(improve_password(password)[1]), improve_password(password)[1]), points_calculator(*character_checker(improve_password(password)[2]), improve_password(password)[2]), points_calculator(*character_checker(improve_password(password)[3]), improve_password(password)[3])]


        for password, score in zip(passwords, scores):
            colu1, colu2 = st.columns([3, 1])  # 3:1 ratio to keep password wider

            with colu1:
                st.code(password, language="")

            with colu2:
                st.markdown(f"<p style='font-size:18px; font-weight:bold; text-align:right;'>Score: {score}/10</p>", unsafe_allow_html=True)



    with col2:
        
        if isinstance(cracking_times, str):  # If it's instantly crackable
            formatted_time = cracking_times
        else:
            formatted_time = "<br>".join([f"**{method}:** {time}" for method, time in cracking_times.items()])

        st.markdown(f"### ⏳ Estimated Time to Crack\n{formatted_time}", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.subheader("🧩 Password Character Breakdown")
        show_interactive_graph(lower, upper, number, symbols)
        
    st.markdown("## 🔒 Security Tips & Best Practices")
    st.write("Here are some important tips to keep your accounts secure:")

    # Tip 1: Use Unique Passwords
    with st.expander("🛡️ Use Unique Passwords for Each Account"):
        st.write("""
        - Never reuse the same password across multiple accounts.
        - If one password gets leaked, all your accounts become vulnerable.
        - Use a **password manager** to store and generate secure passwords.
        """)

    # Tip 2: Enable Two-Factor Authentication
    with st.expander("🔑 Enable Two-Factor Authentication (2FA)"):
        st.write("""
        - Always enable **2FA** on important accounts (email, banking, social media).
        - Prefer **Authenticator Apps** (Google Authenticator, Authy) over SMS codes.
        - This adds an extra layer of security even if your password is stolen.
        """)

    # Tip 3: Watch Out for Phishing
    with st.expander("⚠️ Beware of Phishing Attacks"):
        st.write("""
        - Never click on suspicious links in emails or messages.
        - Verify the sender before entering your password anywhere.
        - Use **browser extensions** like uBlock Origin to block malicious sites.
        """)

    # Tip 4: Update Your Software
    with st.expander("🛠️ Keep Your Software & Apps Updated"):
        st.write("""
        - Always install security updates for your **OS, browsers, and apps**.
        - Hackers exploit outdated software to gain access to your system.
        - Enable **automatic updates** where possible.
        """)

    # Tip 5: Check If Your Email Has Been Leaked
    with st.expander("📌 Check if Your Email is Breached"):
        st.write("""
        - Use [Have I Been Pwned](https://haveibeenpwned.com/) to check if your email was leaked.
        - If your email appears in breaches, **change your password immediately**.
        - Avoid using your main email for less secure websites.
        """)

st.markdown("---")