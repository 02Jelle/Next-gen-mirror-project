from math import sqrt

# Calculates the distance between two colors in RGB space
def color_distance(color1, color2):
  return sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))


# Different theme on which we will base our code to detect outfits
themes = {
  'Funeral': {
      'colors': [(0, 0, 0), (20, 20, 20)]  # Black and dark gray
  },
  'Party': {
      'colors': [(255, 20, 147), (0, 255, 0), (255, 215, 0), (238, 130, 238)]  # Hot pink, green, gold, violet
  },
  'Wedding': {
      'colors': [(255, 255, 255), (255, 240, 245), (245, 200, 241)]  # White, light pink, light pink
  },
  'Office': {
      'colors': [(0, 0, 128), (0, 0, 0), (255, 255, 255), (128, 128, 128)]  # Navy, black, white, gray
  },
  'Casual': {
      'colors': [(200, 200, 200), (255, 255, 255), (255, 0, 0), (0, 0, 255)]  # Light gray, white, red, blue
  },
  'Sporty': {
      'colors': [(255, 165, 0), (0, 128, 0), (128, 0, 128), (255,255,50), (0, 0, 0)]  # Orange, green, purple, lighter yellow, black
  }
}

# Distance to consider a color
distance_threshold = 50


# Give a point to a theme when the color is in the threshold.
def determine_theme(colors):
  theme_scores = {theme: 0 for theme in themes}
  for color in colors:
    for theme, theme_colors in themes.items():
      # Check distance to each color in the theme
      matches = any(color_distance(color, ref_color) < distance_threshold for ref_color in theme_colors['colors'])
      if matches:
        theme_scores[theme] += 1

  # Take the theme with the best score (closest to the outfit)
  best_theme, best_score = max(theme_scores.items(), key=lambda item: item[1])
  return best_theme if best_score > 1 else False


#color_list = [(255, 255, 255), (0, 0, 0),(1,8,3),(250,140,2),(8,250,100)] #change with output tolov3 list color detected
#theme = determine_theme(color_list)
#print(f"The theme of your outfit is: {theme}")
