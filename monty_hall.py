import random
import matplotlib.pyplot as plt # matplotlibをインポート
import japanize_matplotlib  # matplotlibで日本語フォントを使用するためのモジュール

def monty_hall_simulater():
    try:
        num_doors_str = input("ドアの数を入力してください。（3以上の数を入力）>>>")
        num_doors = int(num_doors_str)
        
        if num_doors < 3:
            print("ドアの数は3以上である必要があります。プログラムを終了します。")
        else:
            num_trials_str = input("試行回数を入力してください。>>>")
            num_trials = int(num_trials_str)
            
            if num_trials <= 0:
                print("試行回数は正の整数である必要があります。プログラムを終了します")
            else:
                no_change_wins = 0
                change_wins = 0
                
                for i in range(num_trials):
                    doors = list(range(num_doors))
                    hit_door = random.choice(doors)
                    initial_choice = random.choice(doors)
                    
                    # ドアを変更しない場合
                    final_choice_no_change = initial_choice
                    if final_choice_no_change == hit_door:
                        no_change_wins += 1
                    
                    # ドアを変更する場合
                    monty_can_open = [] # モンティが開けられる外れのドアのリスト
                    for d in doors:
                        if d != initial_choice and d != hit_door:
                            monty_can_open.append(d)
                    
                    # モンティが公開するドアの数は、ドアの総数から最初に選んだドアと正解のドアを除いた数
                    num_to_open = num_doors - 2
                    
                    # モンティが開けられるドアの数が不足している場合、開けられるだけ開ける
                    if num_to_open > len(monty_can_open):
                        num_to_open = len(monty_can_open)

                    monty_opened_doors = random.sample(monty_can_open, num_to_open)
                    
                    possible_final_choices = []
                    for d in doors:
                        if d != initial_choice and d not in monty_opened_doors:
                            possible_final_choices.append(d)
                            
                    # ドアを変更する場合は、残ったドアから一つを選択する
                    # 複数残る場合（ドアが4つ以上の場合）は、均等な確率で選択されると仮定
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