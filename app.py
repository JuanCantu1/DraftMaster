from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

players = []
team_captains = []
remaining_players = []
team_1 = []
team_2 = []
current_turn = 0  # 0 for captain 1's turn, 1 for captain 2's turn

# Load the index.html content
with open('index.html', 'r') as file:
    index_html_content = file.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    global remaining_players, team_1, team_2, current_turn, team_captains, players

    if request.method == 'POST':
        if 'set_players' in request.form:
            players_input = request.form['players']
            players = [player.strip() for player in players_input.split(',') if player.strip()]
            if len(players) != 10:
                return render_template_string(index_html_content, error="Please enter exactly 10 players.", 
                                              team_captains=team_captains, remaining_players=remaining_players,
                                              team_1=team_1, team_2=team_2, current_turn=current_turn,
                                              players=players, team_selection_complete=False, player_entry=True)
        elif 'select_captains' in request.form:
            captain1 = request.form['captain1']
            captain2 = request.form['captain2']
            if captain1 == captain2:
                return render_template_string(index_html_content, error="Captains cannot be the same person.", 
                                              team_captains=team_captains, remaining_players=remaining_players,
                                              team_1=team_1, team_2=team_2, current_turn=current_turn,
                                              players=players, team_selection_complete=False)
            team_captains = [captain1, captain2]
            remaining_players = [person for person in players if person not in team_captains]
            team_1 = [team_captains[0]]
            team_2 = [team_captains[1]]
            current_turn = 0
        elif 'random_captains' in request.form:
            team_captains = random.sample(players, 2)
            remaining_players = [person for person in players if person not in team_captains]
            team_1 = [team_captains[0]]
            team_2 = [team_captains[1]]
            current_turn = 0
        elif 'random_draft' in request.form:
            team_captains = random.sample(players, 2)
            remaining_players = [person for person in players if person not in team_captains]
            team_1 = [team_captains[0]]
            team_2 = [team_captains[1]]
            while remaining_players:
                if current_turn == 0:
                    team_1.append(remaining_players.pop(random.randint(0, len(remaining_players) - 1)))
                    current_turn = 1
                else:
                    team_2.append(remaining_players.pop(random.randint(0, len(remaining_players) - 1)))
                    current_turn = 0
        elif 'pick' in request.form:
            selected_player = request.form['selected_player']
            if selected_player in remaining_players:
                if current_turn == 0:
                    team_1.append(selected_player)
                    current_turn = 1
                else:
                    team_2.append(selected_player)
                    current_turn = 0
                remaining_players.remove(selected_player)
                socketio.emit('update_players', {'team_1': team_1, 'team_2': team_2, 'current_turn': current_turn}, to='/', broadcast=True)
            else:
                return render_template_string(index_html_content, error="Invalid choice. Please try again.", 
                                              team_captains=team_captains, remaining_players=remaining_players,
                                              team_1=team_1, team_2=team_2, current_turn=current_turn,
                                              players=players, team_selection_complete=True)
        elif 'reset' in request.form:
            players = []
            team_captains = []
            remaining_players = []
            team_1 = []
            team_2 = []
            current_turn = 0

    team_selection_complete = len(team_captains) == 2
    player_entry_complete = len(players) == 10
    all_players_picked = len(remaining_players) == 0

    return render_template_string(index_html_content, team_captains=team_captains, remaining_players=remaining_players,
                                  team_1=team_1, team_2=team_2, current_turn=current_turn,
                                  players=players, team_selection_complete=team_selection_complete,
                                  player_entry=not player_entry_complete, all_players_picked=all_players_picked)

if __name__ == '__main__':
    socketio.run(app, debug=True)
