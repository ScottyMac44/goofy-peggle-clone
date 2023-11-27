import json

def generate_plinko_coordinates(rows, cols, spacing, offset):
    coordinates = []

    for row in range(rows):
        for col in range(cols):
            x = col * spacing + offset if row % 2 == 0 else col * spacing + offset + spacing / 2
            y = row * spacing + 250

            if x == screen_size[0]:
                continue
            else:
                coordinates.append((x, y))

    return coordinates

# Set screen size
screen_size = (960,720)

# Set parameters for the plinko pattern
rows = 4
cols = 10
spacing = screen_size[0] / cols # Adjust this value for the desired spacing between pegs
offset = spacing / 2  # Adjust this value for the desired horizontal offset

# Generate peg coordinates
peg_coordinates = generate_plinko_coordinates(rows, cols, spacing, offset)
json_contents = {"level_0" : {
    "background" : "path",
    "peg_positions" : peg_coordinates
}}
# Save coordinates to a JSON file
with open("levels.json", "w") as file:
    json.dump(json_contents, file)

print(f"Generated {len(peg_coordinates)} peg coordinates.")