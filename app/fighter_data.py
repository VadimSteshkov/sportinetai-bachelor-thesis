from app import st,difflib,pd,px
# Function to display a fighter's profile
def display_fighter_profile(fighter_profile, fighter_name):
    """
    Displays the fighter's profile in a reduced-size block.

    :param fighter_profile: Dictionary containing fighter data.
    :param fighter_name: The fighter's name.
    """
    profile_info = fighter_profile.get('profile_info', 'No information available.')
    image_url = fighter_profile.get('image_url', None)

    # Fighter Profile Block
    st.markdown(
        f"""
        <div style="background-color: #1a1a1a; padding: 15px; border-radius: 8px; margin: 10px; width: 100%;">
            <div style="display: flex; flex-direction: row; align-items: center; gap: 20px;">
                <img src="{image_url}" alt="{fighter_name.title()}" style="width: 280px; height: auto; border-radius: 10px;">
                <div>
                    <h3 style="color: #ffffff; margin: 0;">{fighter_name.title()}</h3>
                    <p style="color: #d3d3d3; font-size: 14px; margin: 5px 0;">{profile_info}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# Функция для поиска ближайшего совпадения
def find_closest_fighter(name, dataset):
    all_fighters = (
            dataset['r_fighter'].str.strip().str.lower().tolist() +
            dataset['b_fighter'].str.strip().str.lower().tolist()
    )
    closest_match = difflib.get_close_matches(name.strip().lower(), all_fighters, n=1, cutoff=0.6)
    return closest_match[0] if closest_match else None
def calculate_fighter_stats(fighter_name, ufc_dataset):
    """
    Вычисляет статистику по количеству боев и побед для указанного бойца.
    """
    # Количество боев за красный угол
    r_fights = ufc_dataset[ufc_dataset['r_fighter'].str.lower() == fighter_name.lower()].shape[0]
    # Количество побед за красный угол
    r_wins = ufc_dataset[
        (ufc_dataset['r_fighter'].str.lower() == fighter_name.lower()) &
        (ufc_dataset['winner'] == 'Red')
    ].shape[0]

    # Количество боев за синий угол
    b_fights = ufc_dataset[ufc_dataset['b_fighter'].str.lower() == fighter_name.lower()].shape[0]
    # Количество побед за синий угол
    b_wins = ufc_dataset[
        (ufc_dataset['b_fighter'].str.lower() == fighter_name.lower()) &
        (ufc_dataset['winner'] == 'Blue')
    ].shape[0]

    # Общее количество боёв
    total_fights = r_fights + b_fights

    # Процент побед за красный угол
    r_win_rate = round((r_wins / total_fights) * 100, 2) if r_fights > 0 else 0
    # Процент побед за синий угол
    b_win_rate = round((b_wins / total_fights) * 100, 2) if b_fights > 0 else 0

    return {
        "r_fights": r_fights,
        "b_fights": b_fights,
        "r_wins": r_wins,
        "b_wins": b_wins,
        "r_win_rate": r_win_rate,
        "b_win_rate": b_win_rate
    }

#
def process_fighter_data(fighter_name, ufc_dataset, enable_name_suggestion):
    """
    Process fighter data based on user input and dataset.
    If name suggestion is disabled, rely on user input for dataset lookup.
    """
    fighter_list = (
        ufc_dataset['r_fighter'].str.strip().str.lower().tolist() +
        ufc_dataset['b_fighter'].str.strip().str.lower().tolist()
    )

    if enable_name_suggestion:
        # Find the closest match
        closest_match = difflib.get_close_matches(fighter_name.strip().lower(), fighter_list, n=1, cutoff=0.6)
        if closest_match:
            return closest_match[0]
        else:
            return None
    else:
        # Directly return the user input (as lowercased for dataset lookup)
        return fighter_name.strip().lower()
# Function to display Stats Block
def display_stats_block(stats_data, fighter_name):
    """
    Displays the fighter's stats in a clean and simple horizontal layout.

    :param stats_data: Dictionary containing stats and metrics.
    :param fighter_name: Name of the fighter.
    """

    # Extract statistics
    wins_ko = stats_data.get("wins_ko", "N/A")
    wins_sub = stats_data.get("wins_sub", "N/A")
    first_round_finishes = stats_data.get("first_round_finishes", "N/A")
    striking_accuracy = stats_data.get("striking_accuracy", "N/A")
    strikes_landed = stats_data.get("strikes_landed", "N/A")
    strikes_attempted = stats_data.get("strikes_attempted", "N/A")
    takedown_accuracy = stats_data.get("takedown_accuracy", "N/A")
    takedown_landed = stats_data.get("takedowns_landed", "N/A")
    takedown_attempted = stats_data.get("takedowns_attempted", "N/A")


    # Header
    st.markdown(f"### Stats & Records for {fighter_name.title()}")

    # Block 1: Wins and Finishes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"<h4 style='text-align: center;'>{wins_ko}</h4><p style='text-align: center;'>Wins by Knockout</p>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<h4 style='text-align: center;'>{wins_sub}</h4><p style='text-align: center;'>Wins by Submission</p>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"<h4 style='text-align: center;'>{first_round_finishes}</h4><p style='text-align: center;'>First Round Finishes</p>",
            unsafe_allow_html=True,
        )

    # Block 2: Striking and Takedown Accuracy
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div style="background-color: #1a1a1a; padding: 15px; border-radius: 8px; text-align: center;">
                <h4 style="color: white;">Striking Accuracy</h4>
                <p style="color: red; font-size: 24px; margin: 10px 0;">{striking_accuracy}</p>
                <p style="color: #d3d3d3;">Sig. Strikes Landed: {strikes_landed}<br>Sig. Strikes Attempted: {strikes_attempted}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div style="background-color: #1a1a1a; padding: 15px; border-radius: 8px; text-align: center;">
                <h4 style="color: white;">Takedown Accuracy</h4>
                <p style="color: red; font-size: 24px; margin: 10px 0;">{takedown_accuracy}</p>
                <p style="color: #d3d3d3;">Takedowns Landed: {takedown_landed}<br>Takedowns Attempted: {takedown_attempted}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    # Block 4: Significant Strikes by Target
    if 'strikes_by_target_svg' in stats_data:
        st.markdown(
            """
            <div style="background-color: #1a1a1a; padding: 15px; border-radius: 8px; text-align: center; margin-top: 20px;">
                <h4 style="color: white;">Significant Strikes by Target</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

        svg_content = stats_data['strikes_by_target_svg']

        if svg_content and svg_content != "No SVG available." and svg_content != "No SVG section found.":
            # Обернуть SVG в div с фоном
            st.markdown(
                f"""
                <div style="background-color: rgb(26, 26, 26); ; padding: 20px; border-radius: 8px; margin-top: 10px; text-align: center;">
                    {svg_content}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Сообщение об ошибке, если SVG недоступен
            st.markdown(
                """
                <div style="text-align: center; color: red; margin-top: 15px;">
                    No SVG diagram available for this fighter.
                </div>
                """,
                unsafe_allow_html=True,
            )

def display_features_with_corner_stats(fighter1_name, fighter2_name, ufc_dataset):
    """
    Вычисляет таблицу признаков и отображает данные в виде таблицы или диаграмм на основе выбора.
    """
    fighter1_stats = calculate_fighter_stats(fighter1_name, ufc_dataset)
    fighter2_stats = calculate_fighter_stats(fighter2_name, ufc_dataset)

    # Формируем DataFrame для отображения
    data = {
        "Feature": [
            "Total Fights (Red Corner)", "Win Rate (Red Corner)", "Wins (Red Corner)",
            "Total Fights (Blue Corner)", "Win Rate (Blue Corner)", "Wins (Blue Corner)"
        ],
        fighter1_name: [
            fighter1_stats["r_fights"], f"{fighter1_stats['r_win_rate']}%", fighter1_stats["r_wins"],
            fighter1_stats["b_fights"], f"{fighter1_stats['b_win_rate']}%", fighter1_stats["b_wins"]
        ],
        fighter2_name: [
            fighter2_stats["r_fights"], f"{fighter2_stats['r_win_rate']}%", fighter2_stats["r_wins"],
            fighter2_stats["b_fights"], f"{fighter2_stats['b_win_rate']}%", fighter2_stats["b_wins"]
        ]
    }
    features_df = pd.DataFrame(data)

    # Рассчитываем проценты побед для бойца 1
    fighter1_total_fights = fighter1_stats["r_fights"] + fighter1_stats["b_fights"]
    fighter1_red_win_ratio = (
                fighter1_stats["r_wins"] / fighter1_total_fights * 100) if fighter1_total_fights > 0 else 0
    fighter1_blue_win_ratio = (
                fighter1_stats["b_wins"] / fighter1_total_fights * 100) if fighter1_total_fights > 0 else 0

    # Рассчитываем проценты побед для бойца 2
    fighter2_total_fights = fighter2_stats["r_fights"] + fighter2_stats["b_fights"]
    fighter2_red_win_ratio = (
                fighter2_stats["r_wins"] / fighter2_total_fights * 100) if fighter2_total_fights > 0 else 0
    fighter2_blue_win_ratio = (
                fighter2_stats["b_wins"] / fighter2_total_fights * 100) if fighter2_total_fights > 0 else 0

    # Круговая диаграмма для бойца 1
    fig1 = px.pie(
        names=["Red Corner", "Blue Corner"],
        values=[fighter1_red_win_ratio, fighter1_blue_win_ratio],  # Используем проценты побед
        title=f"{fighter1_name.title()} Corner Win Rate",
        color=["Red Corner", "Blue Corner"],  # Обозначаем цвета для каждой категории
        color_discrete_map={"Red Corner": "red", "Blue Corner": "blue"}  # Указываем цвета
    )

    # Настройка текста на диаграмме
    fig1.update_traces(
        text=[f"{fighter1_red_win_ratio:.2f}%", f"{fighter1_blue_win_ratio:.2f}%"],  # Указываем текст
        textinfo="text",  # Показываем только указанный текст
        hoverinfo="label+text"  # Подсказка с названием угла и процентом побед
    )

    # Круговая диаграмма для бойца 2
    fig2 = px.pie(
        names=["Red Corner", "Blue Corner"],
        values=[fighter2_red_win_ratio, fighter2_blue_win_ratio],  # Используем проценты побед
        title=f"{fighter2_name.title()} Corner Win Rate",
        color=["Red Corner", "Blue Corner"],  # Обозначаем цвета для каждой категории
        color_discrete_map={"Red Corner": "red", "Blue Corner": "blue"}  # Указываем цвета
    )

    # Настройка текста на диаграмме
    fig2.update_traces(
        text=[f"{fighter2_red_win_ratio:.2f}%", f"{fighter2_blue_win_ratio:.2f}%"],
        textinfo="text",
        hoverinfo="label+text"
    )

    # Добавляем выбор отображения
    display_option = st.radio(
        "Choose display format:",
        options=["Table", "Charts"],
        index=1
    )

    if display_option == "Table":
        # Выводим таблицу
        st.markdown("### Fighter Corner Stats")
        st.table(features_df)
    elif display_option == "Charts":
        # Выводим диаграммы
        st.markdown("### Fighter Corner Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.plotly_chart(fig2, use_container_width=True)

    return features_df