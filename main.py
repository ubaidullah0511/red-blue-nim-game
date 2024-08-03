import sys

def display_tokens(red_tokens, blue_tokens):
    
    # Displays the current number of red and blue tokens.
   
    print(f"Red tokens: {red_tokens}, Blue tokens: {blue_tokens}")

def player_turn(player, red_tokens, blue_tokens):
    
    # Handles the player's turn, prompting for color and number of tokens to remove.
    # Validates the input and updates the token counts.
    
    print(f"Player {player}'s turn")
    
    color = input("Choose a color (red/blue): ").strip().lower()
    while color not in ["red", "blue"]:
        color = input("Invalid color. Choose a color (red/blue): ").strip().lower()
    
    count = int(input("How many tokens to remove (1, 2, or 3)? "))
    while count not in [1, 2, 3]:
        count = int(input("Invalid number of tokens. Choose 1, 2, or 3: "))

    if color == "red":
        if red_tokens >= count:
            red_tokens -= count
        else:
            print(f"Not enough red tokens to remove {count}.")
            return player_turn(player, red_tokens, blue_tokens)
    
    else:
        if blue_tokens >= count:
            blue_tokens -= count
        else:
            print(f"Not enough blue tokens to remove {count}.")
            return player_turn(player, red_tokens, blue_tokens)
    
    return red_tokens, blue_tokens

def check_winner_standard(red_tokens, blue_tokens):
    
    # Determines if the game has ended in the standard version, where either pile is empty.
    
    return red_tokens == 0 or blue_tokens == 0

def check_winner_misere(red_tokens, blue_tokens):
    
    # Determines if the game has ended in the misère version, where either pile is empty.
    
    return red_tokens == 0 or blue_tokens == 0

def calculate_score(red_tokens, blue_tokens):
   
    # Calculates the score based on the remaining tokens.
    # Each red token is worth 2 points, each blue token is worth 3 points.
    
    return red_tokens * 2 + blue_tokens * 3

def minimax(red_tokens, blue_tokens, depth, is_maximizing, alpha, beta, version):
   
    # Implements the Minimax algorithm with Alpha-Beta Pruning to determine the optimal move.
    
    # Parameters:
    # - red_tokens, blue_tokens: Current state of tokens.
    # - depth: Remaining search depth.
    # - is_maximizing: Boolean indicating if the current player is maximizing.
    # - alpha, beta: Alpha-Beta values for pruning.
    # - version: Game version ('standard' or 'misere').

    # Returns:
    # - Evaluated score for the current game state.
    
    if (version == 'standard' and check_winner_standard(red_tokens, blue_tokens)) or \
       (version == 'misere' and check_winner_misere(red_tokens, blue_tokens)) or depth == 0:
        return calculate_score(red_tokens, blue_tokens)

    if is_maximizing:
        max_eval = float('-inf')
        for count in [1, 2, 3]:
            if red_tokens >= count:
                eval = minimax(red_tokens - count, blue_tokens, depth - 1, False, alpha, beta, version)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return max_eval
            
            if blue_tokens >= count:
                eval = minimax(red_tokens, blue_tokens - count, depth - 1, False, alpha, beta, version)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return max_eval
        
        return max_eval
    
    else:
        min_eval = float('inf')
        for count in [1, 2, 3]:
            if red_tokens >= count:
                eval = minimax(red_tokens - count, blue_tokens, depth - 1, True, alpha, beta, version)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    return min_eval
            
            if blue_tokens >= count:
                eval = minimax(red_tokens, blue_tokens - count, depth - 1, True, alpha, beta, version)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    return min_eval
        
        return min_eval

def computer_turn(red_tokens, blue_tokens, depth, version):
    
    # Determines the computer's optimal move using the Minimax algorithm.
   
    best_score = float('-inf')
    best_move = None
    
    for count in [1, 2, 3]:
        if red_tokens >= count:
            score = minimax(red_tokens - count, blue_tokens, depth - 1, False, float('-inf'), float('inf'), version)
            if score > best_score:
                best_score = score
                best_move = ('red', count)
        
        if blue_tokens >= count:
            score = minimax(red_tokens, blue_tokens - count, depth - 1, False, float('-inf'), float('inf'), version)
            if score > best_score:
                best_score = score
                best_move = ('blue', count)
    
    if best_move is None:
        print("No valid moves available for computer.")
        return red_tokens, blue_tokens
    
    color, count = best_move
    if color == 'red':
        red_tokens -= count
    else:
        blue_tokens -= count
    
    print(f"Computer removes {count} {color} tokens.")
    return red_tokens, blue_tokens

def red_blue_nim_game():
    
    # Main function to start the game, handle user input, and control game flow.
    
    if len(sys.argv) < 4:
        print("Usage: python <name_of_the_file> <num-red> <num-blue> <version> [<first-player> <depth>]")
        print("Examples:")
        print("  python <name_of_the_file> 10 10 standard computer 3")
        print("  python <name_of_the_file> 10 10 misere")
        print("  python <name_of_the_file> 10 10 standard")
        return
    
    red_tokens = int(sys.argv[1])
    blue_tokens = int(sys.argv[2])
    version = sys.argv[3].lower()
    first_player = sys.argv[4].lower() if len(sys.argv) > 4 else 'computer'
    depth = int(sys.argv[5]) if len(sys.argv) > 5 else 3

    current_player = 1 if first_player == 'human' else 2

    if version not in ['standard', 'misere']:
        print("Invalid game version. Choose 'standard' or 'misere'.")
        return

    while True:
        display_tokens(red_tokens, blue_tokens)
        
        if current_player == 1:
            red_tokens, blue_tokens = player_turn("Human", red_tokens, blue_tokens)
        
        else:
            red_tokens, blue_tokens = computer_turn(red_tokens, blue_tokens, depth, version)

        if (version == 'standard' and check_winner_standard(red_tokens, blue_tokens)) or \
           (version == 'misere' and check_winner_misere(red_tokens, blue_tokens)):
            print(f"Player {current_player} wins!")
            break
        
        current_player = 2 if current_player == 1 else 1

    score = calculate_score(red_tokens, blue_tokens)
    print(f"Final score: {score} points")

if __name__ == "__main__":
    red_blue_nim_game()
