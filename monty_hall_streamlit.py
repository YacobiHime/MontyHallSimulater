import random
import matplotlib.pyplot as plt
import streamlit as st
import japanize_matplotlib

# Streamlitのページ設定
st.set_page_config(layout="wide") # ページ全体を使う設定
st.title("モンティホール問題シミュレーション") # アプリのタイトル

# フォント設定 (Streamlitではパスを指定する必要が無いらしいが、一応残しておく)
# font_path = "fonts/NotoSerifJP-Regular.ttf" # アプリ実行環境にフォントファイルを置く
# plt.rcParams['font.family'] = 'Noto Serif JP'
# plt.rcParams["font.sans-serif"] = "Noto Serif JP"
plt.rcParams['axes.unicode_minus'] = False

# モンティホール問題のシミュレーションを行う関数
def monty_hall_simulater_streamlit(num_doors, num_trials):
    no_change_wins = 0
    change_wins = 0

    for i in range(num_trials): # 試行回数分ループ
        doors = list(range(num_doors)) # ドアのリストを作成
        hit_door = random.choice(doors) # 正解のドアをランダムに選択
        initial_choice = random.choice(doors) # 最初に選択するドアをランダムに選択

        # ドアを変更しない場合
        final_choice_no_change = initial_choice # 最初に選んだドアをそのまま選択
        if final_choice_no_change == hit_door:
            no_change_wins += 1 # もし最後に選択していたドアが当たりなら、変更せずに正解した回数を1追加

        # ドアを変更する場合
        monty_can_open = [] # モンティが開けられる外れのドアのリスト
        for d in doors:
            if d != initial_choice and d != hit_door:
                monty_can_open.append(d)

        # もしモンティが開ける外れのドアの数が、モンティが開けられるドアの数よりも大きいなら、モンティは全ての外れのドアを開ける
        num_to_open = num_doors - 2
        if num_to_open > len(monty_can_open):
            num_to_open = len(monty_can_open)

        # 外れのドアがない場合はエラーになるので、monty_opened_doorsを空リストにする
        if monty_can_open:
            monty_opened_doors = random.sample(monty_can_open, min(num_to_open, len(monty_can_open)))
        else:
            monty_opened_doors = []

        possible_final_choices = []
        for d in doors:
            if d != initial_choice and d not in monty_opened_doors:
                possible_final_choices.append(d)

        # ドアを変更する場合は、残ったドアから一つを選択する
        # 残りのドアがない場合はスキップ（理論上、残りのドアは発生しないはず）
        if possible_final_choices:
            final_choice_change = random.choice(possible_final_choices)
            if final_choice_change == hit_door:
                change_wins += 1 # もし最後に選択していたドアが当たりなら、変更して正解した回数を1追加

    return no_change_wins, change_wins # シミュレーション結果を返す

# StreamlitのUI要素
st.sidebar.header("シミュレーション設定")
num_doors = st.sidebar.slider("ドアの数", min_value=3, max_value=100, value=3, step=1)
num_trials = st.sidebar.number_input("試行回数", min_value=1, max_value=100000, value=1000, step=100)

if st.sidebar.button("シミュレーション実行"):
    if num_doors < 3:
        st.error("ドアの数は3以上である必要があります。")
    elif num_trials <= 0:
        st.error("試行回数は正の整数である必要があります。")
    else:
        with st.spinner("シミュレーション中..."): # 処理中にスピナーを表示
            no_change_wins, change_wins = monty_hall_simulater_streamlit(num_doors, num_trials)

        st.subheader(f"シミュレーションの結果（ドアの数: {num_doors}、試行回数: {num_trials}回）:")

        col1, col2 = st.columns(2) # 2つのカラムで表示

        with col1:
            st.write("--- ドアを変更しなかった場合 ---")
            st.write(f"正解した回数: **{no_change_wins}回**")
            st.write(f"正解した確率: **{no_change_wins / num_trials:.2%}**")

        with col2:
            st.write("--- ドアを変更した場合 ---")
            st.write(f"正解した回数: **{change_wins}回**")
            st.write(f"正解した確率: **{change_wins / num_trials:.2%}**")

        # --- グラフの作成 ---
        labels = ['変更しない', '変更する']
        wins = [no_change_wins, change_wins]
        win_probabilities = [no_change_wins / num_trials, change_wins / num_trials]

        fig, axes = plt.subplots(1, 2, figsize=(12, 5)) # 2つのサブプロットを作成

        # 正解回数の棒グラフ
        axes[0].bar(labels, wins, color=['skyblue', 'lightcoral'])
        axes[0].set_ylabel('正解回数')
        axes[0].set_title('モンティホール問題 シミュレーション結果 (正解回数)')
        axes[0].grid(axis='y', linestyle='--')

        # 正解確率の棒グラフ
        axes[1].bar(labels, win_probabilities, color=['skyblue', 'lightcoral'])
        axes[1].set_ylabel('正解確率')
        axes[1].set_title('モンティホール問題 シミュレーション結果 (正解確率)')
        axes[1].set_ylim(0, 1) # 確率なのでY軸の範囲を0から1に設定
        for i, v in enumerate(win_probabilities):
            axes[1].text(i, v + 0.02, f"{v:.2%}", ha='center', va='bottom') # 確率の値を表示
        axes[1].grid(axis='y', linestyle='--')

        plt.tight_layout() # レイアウトを調整
        st.pyplot(fig) # Streamlitでmatplotlibのグラフを表示