import random
import matplotlib.pyplot as plt # matplotlibをインポート

font_path = "fonts/NotoSerifJP-Regular.ttf"

plt.rcParams['font.family'] = 'Noto Serif JP' # フォント設定
plt.rcParams["font.sans-serif"] = "Noto Serif JP" # サンセリフフォント設定
plt.rcParams['axes.unicode_minus'] = False # マイナス記号の表示設定

# モンティホール問題のシミュレーションを行う関数
def monty_hall_simulater():
    try:
        num_doors_str = input("ドアの数を入力してください。（3以上の数を入力）>>>")
        num_doors = int(num_doors_str)
        
        if num_doors < 3:
            print("ドアの数は3以上である必要があります。プログラムを終了します。")
        else:
            num_trials = int(input("試行回数を入力してください。>>>"))
            
            if num_trials <= 0:
                print("試行回数は正の整数である必要があります。プログラムを終了します")
            else:
                no_change_wins = 0
                change_wins = 0
                
                for i in range(num_trials): # 試行回数分ループ
                    doors = list(range(num_doors)) # ドアのリストを作成
                    hit_door = random.choice(doors) # 正解のドアをランダムに選択
                    initial_choice = random.choice(doors) # 挑戦者が最初に選択するドアをランダムに選択
                    
                    # ドアを変更しない場合
                    final_choice_no_change = initial_choice # 最初に選んだドアをそのまま選択
                    if final_choice_no_change == hit_door:
                        no_change_wins += 1 # もし最後に選択していたドアが当たりだった場合変更せずに正解した回数を1追加
                    
                    # ドアを変更する場合
                    monty_can_open = [] # モンティが開けられる外れのドアのリスト
                    # 最初に選択したドアと正解のドアを避けて、外れのドアリストを作成
                    for d in doors:
                        if d != initial_choice and d != hit_door:
                            monty_can_open.append(d)

                    num_to_open = num_doors - 2 # モンティが開けるべき外れのドアの数

                    # 念の為、モンティが開けるドアの数がドアの数よりも大きい場合は、モンティが開けられるドアの数に設定
                    if num_to_open > len(monty_can_open):
                        num_to_open = len(monty_can_open)
                    
                    # モンティが開けられるドアと、開けるべきドアの2つから、モンティが実際に開けたドアのリストを作成
                    monty_opened_doors = random.sample(monty_can_open, num_to_open)
                    
                    # 最初に選んだドアとモンティが開けたドアを除外して、選びなおせるドアのリストを作成
                    possible_final_choices = []
                    for d in doors:
                        if d != initial_choice and d not in monty_opened_doors:
                            possible_final_choices.append(d)
                            
                    # ドアを変更する場合は、選び直せるドアのリストから一つを選択する
                    final_choice_change = random.choice(possible_final_choices) 
                    
                    if final_choice_change == hit_door:
                        change_wins += 1

                print(f"\nシミュレーションの結果（ドアの数: {num_doors}回）、試行回数: {num_trials}回 :")
                print(f"--- ドアを変更しなかった場合 ---")
                print(f"正解した回数: {no_change_wins}回")
                print(f"正解した確率: {no_change_wins / num_trials:.2%}")

                print(f"--- ドアを変更した場合 ---")
                print(f"正解した回数: {change_wins}回")
                print(f"正解した確率: {change_wins / num_trials:.2%}")

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
                plt.show() # グラフを表示

    except ValueError:
        print("無効な入力です。整数を入力してください。")
    
    except Exception as e:
        print(f"予期せぬエラーが発生しました。: {e}")

monty_hall_simulater()