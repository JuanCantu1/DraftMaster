from flask import Flask, render_template_string, request, flash
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

class TeamDraft:
    def __init__(self):
        self.players = []
        self.team_captains = []
        self.remaining_players = []
        self.team_1 = []
        self.team_2 = []
        self.current_turn = 0  # 0 for captain 1's turn, 1 for captain 2's turn

    def reset(self):
        self.players = []
        self.team_captains = []
        self.remaining_players = []
        self.team_1 = []
        self.team_2 = []
        self.current_turn = 0

team_draft = TeamDraft()

# Load the index.html content
with open('index.html', 'r') as file:
    index_html_content = file.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    global team_draft

    if request.method == 'POST':
        if 'set_players' in request.form:
            players_input = request.form['players']
            team_draft.players = [player.strip() for player in players_input.split(',') if player.strip()]
            if len(team_draft.players) != 10:
                flash("Please enter exactly 10 players.")
                return render_template_string(index_html_content, **get_context())
        elif 'select_captains' in request.form:
            captain1 = request.form['captain1']
            captain2 = request.form['captain2']
            if captain1 == captain2:
                flash("Captains cannot be the same person.")
                return render_template_string(index_html_content, **get_context())
            team_draft.team_captains = [captain1, captain2]
            team_draft.remaining_players = [person for person in team_draft.players if person not in team_draft.team_captains]
            team_draft.team_1 = [team_draft.team_captains[0]]
            team_draft.team_2 = [team_draft.team_captains[1]]
            team_draft.current_turn = 0
        elif 'random_captains' in request.form:
            team_draft.team_captains = random.sample(team_draft.players, 2)
            team_draft.remaining_players = [person for person in team_draft.players if person not in team_draft.team_captains]
            team_draft.team_1 = [team_draft.team_captains[0]]
            team_draft.team_2 = [team_draft.team_captains[1]]
            team_draft.current_turn = 0
        elif 'random_draft' in request.form:
            team_draft.team_captains = random.sample(team_draft.players, 2)
            team_draft.remaining_players = [person for person in team_draft.players if person not in team_draft.team_captains]
            team_draft.team_1 = [team_draft.team_captains[0]]
            team_draft.team_2 = [team_draft.team_captains[1]]
            while team_draft.remaining_players:
                if team_draft.current_turn == 0:
                    team_draft.team_1.append(team_draft.remaining_players.pop(random.randint(0, len(team_draft.remaining_players) - 1)))
                    team_draft.current_turn = 1
                else:
                    team_draft.team_2.append(team_draft.remaining_players.pop(random.randint(0, len(team_draft.remaining_players) - 1)))
                    team_draft.current_turn = 0
        elif 'pick' in request.form:
            selected_player = request.form['selected_player']
            if selected_player in team_draft.remaining_players:
                if team_draft.current_turn == 0:
                    team_draft.team_1.append(selected_player)
                    team_draft.current_turn = 1
                else:
                    team_draft.team_2.append(selected_player)
                    team_draft.current_turn = 0
                team_draft.remaining_players.remove(selected_player)
                socketio.emit('update_players', {'team_1': team_draft.team_1, 'team_2': team_draft.team_2, 'current_turn': team_draft.current_turn}, to='/')
            else:
                flash("Invalid choice. Please try again.")
                return render_template_string(index_html_content, **get_context())
        elif 'reset' in request.form:
            team_draft.reset()

    return render_template_string(index_html_content, **get_context())

def get_context():
    return {
        'team_captains': team_draft.team_captains,
        'remaining_players': team_draft.remaining_players,
        'team_1': team_draft.team_1,
        'team_2': team_draft.team_2,
        'current_turn': team_draft.current_turn,
        'players': team_draft.players,
        'team_selection_complete': len(team_draft.team_captains) == 2,
        'player_entry': len(team_draft.players) != 10,
        'all_players_picked': len(team_draft.remaining_players) == 0
    }

if __name__ == '__main__':
    socketio.run(app, debug=True)
