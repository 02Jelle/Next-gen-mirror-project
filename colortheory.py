import math
def rgb_to_hsl(listForm): # https://www.30secondsofcode.org/python/s/hex-to-rgb/ # https://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/
	red = listForm[0]/255
	green = listForm[1]/255
	blue = listForm[2]/255
	minimum = min([red, green, blue])
	maximum = max([red, green, blue])
	luminance = (minimum + maximum)/2
	if maximum != minimum:
		if luminance <= 0.5:
			saturation = (maximum - minimum)/(maximum + minimum)
		else:
			saturation = (maximum - minimum)/(2.0 - maximum - minimum)
		if maximum == red:
			hue = (green - blue)/(maximum - minimum)
		elif maximum == green:
			hue = 2.0 + (blue - red)/(maximum - minimum)
		else:
			hue = 4.0 + (red - green)/(maximum - minimum)
		hue = hue * 60
	else:
		saturation = 0
		hue = 0
	return [math.ceil(hue), math.ceil(saturation * 100), math.ceil(luminance * 100)]
def color_difference_formula(color1, color2): # https://www.101computing.net/colour-difference-formula/
	distance = math.sqrt(((color2[0] - color1[0]))**2 + ((color2[1] - color1[1]))**2 + ((color2[2] - color1[2]))**2)
	return distance
def closest_color(color):
    dark_yellow = [163, 181, 0, 'dark yellow']
    yellow = [255, 255, 0, 'yellow']
    light_yellow = [255, 255, 110, 'light yellow']
    dark_blue = [0, 0, 181, 'dark blue']
    blue = [0, 0, 255, 'blue']
    light_blue = [208, 212, 255, 'light blue']
    dark_green = [0, 181, 54, 'dark green']
    green = [0, 255, 0, 'green']
    light_green = [129, 255, 110, 'light green']
    dark_purple = [144, 0, 181, 'dark purple']
    purple = [255, 0, 255, 'purple']
    light_purple = [243, 208, 255, 'light purple']
    dark_aqua = [0, 181, 175, 'dark aqua']
    aqua = [0, 255, 255, 'aqua']
    light_aqua = [208, 255, 254, 'light aqua']
    #dark_red = [159, 0, 0, 'dark red']
    red = [255, 0, 0, 'red']
    light_red = [255, 208, 208, 'light red']
    white = [255, 255, 255, 'white']
    black = [0, 0, 0, 'black']
    gray = [208, 208, 208, 'gray']
    dark_orange = [181, 138, 0, 'dark orange']
    orange = [255, 171, 0, 'orange']
    light_orange = [255, 238, 208, 'light orange']
    brown = [127, 54, 6, 'brown']
    dark_pink = [181, 0, 138, 'dark pink']
    pink = [255, 0, 162, 'pink']
    light_pink = [255, 208, 238, 'light pink']
    colors = [dark_yellow, yellow, light_yellow, dark_blue, blue, light_blue, dark_green, green, light_green, dark_purple, purple, light_purple, dark_aqua, aqua, light_aqua, red, light_red, gray, dark_orange, orange, light_orange, dark_pink, pink, light_pink]
    if color[0] in range(200, 255) and color[1] in range(200, 255) and color[2] in range(200, 255):
    	return white
    if color[0] in range(0, 20) and color[1] in range(0, 20) and color[2] in range(0, 20):
    	return black
    minimum = 10000
    min_color = ""
    for i in colors:
    	if color_difference_formula(i, color) < minimum:
    		min_color = i
    		minimum = color_difference_formula(i, color)
    return min_color
def complementary(color1, color2): # https://rgbcolorpicker.com/complementary # https://dev.to/madsstoumann/colors-are-math-how-they-match-and-how-to-build-a-color-picker-4ei8
	hue1 = convert_to_angle(color1[0])
	hue2 = convert_to_angle(color2[0])
	saturation1 = color1[1]
	saturation2 = color2[1]
	luminance1 = color1[2]
	luminance2 = color2[2]
	if hue1 in range(hue2 + 160, hue2 + 200):
		print("Complementary colors")
		return True
	elif hue1 == hue2 and hue1 == 0 and saturation1 == 0 and saturation2 == 0: # for blacks, whites, and gray hues
		print("Complementary colors")
		return True
	else:
		return False
def convert_to_angle(angle): # https://www.math10.com/en/geometry/angles/measure/angles-and-measurement.html#:~:text=Given%20a%20negative%20angle%2C%20we%20add%20360,get%20its%20corresponding%20positive%20angle.
	if angle >= 360:
		return (angle - 360)
	elif angle < 0:
		return (angle + 360)
	else:
		return angle
def split_complementary(color1, color2, color3): # https://www.sessions.edu/color-calculator/ # https://dev.to/madsstoumann/colors-are-math-how-they-match-and-how-to-build-a-color-picker-4ei8
	hue1 = convert_to_angle(color1[0])
	hue2 = convert_to_angle(color2[0])
	hue3 = convert_to_angle(color3[0])
	saturation1 = color1[1]
	saturation2 = color2[1]
	saturation3 = color3[1]
	luminance1 = color1[2]
	luminance2 = color2[2]
	luminance3 = color3[2]
	if hue2 in range(convert_to_angle(hue1 + 130), convert_to_angle(hue1 + 180)) and hue3 in range(convert_to_angle(hue1 + 180), convert_to_angle(hue1 + 230)):
		print("Split Complementary Colors")
		return True
	elif hue3 in range(convert_to_angle(hue1 + 130), convert_to_angle(hue1 + 180)) and hue2 in range(convert_to_angle(hue1 + 180), convert_to_angle(hue1 + 230)):
		print("Split Complementary Colors")
		return True
	elif hue1 in range(convert_to_angle(hue2 + 130), convert_to_angle(hue2 + 180)) and hue3 in range(convert_to_angle(hue2 + 180), convert_to_angle(hue2 + 230)):
		print("Split Complementary Colors")
		return True
	elif hue3 in range(convert_to_angle(hue2 + 130), convert_to_angle(hue2 + 180)) and hue1 in range(convert_to_angle(hue2 + 180), convert_to_angle(hue2 + 230)):
		print("Split Complementary Colors")
		return True
	elif hue1 in range(convert_to_angle(hue3 + 130), convert_to_angle(hue3 + 180)) and hue2 in range(convert_to_angle(hue3 + 180), convert_to_angle(hue3 + 230)):
		print("Split Complementary Colors")
		return True
	elif hue2 in range(convert_to_angle(hue3 + 130), convert_to_angle(hue3 + 180)) and hue1 in range(convert_to_angle(hue3 + 180), convert_to_angle(hue3 + 230)):
		print("Split Complementary Colors")
		return True
	else:
		return False
def analogous_colors(colors): # https://www.sessions.edu/color-calculator/ # https://dev.to/madsstoumann/colors-are-math-how-they-match-and-how-to-build-a-color-picker-4ei8
	if len(colors) < 2:
		print("There are less than 2 colors provided, can not check")
		return False
	elif len(colors) == 2:
		color1 = colors[0]
		color2 = colors[1]
		hue1 = convert_to_angle(color1[0])
		hue2 = convert_to_angle(color2[0])
		if(hue1 in range(hue2 - 31, hue2 + 31)):
			print("Analogous Colors")
			return True
		elif(hue2 in range(hue1 - 31, hue1 + 31)):
			print("Analogous Colors")
			return True
		else:
			return False
	elif len(colors) == 3:
		color1 = colors[0]
		color2 = colors[1]
		color3 = colors[2]
		hue1 = convert_to_angle(color1[0])
		hue2 = convert_to_angle(color2[0])
		hue3 = convert_to_angle(color3[0])
		if(hue2 in range(hue1 - 31, hue1 + 31) and hue3 in range(hue1 - 31, hue1 + 31)):
			print("Analogous Colors")
			return True
		elif(hue1 in range(hue2 - 31, hue2 + 31) and hue3 in range(hue2 - 31, hue2 + 31)):
			print("Analogous Colors")
			return True
		elif(hue1 in range(hue3 - 31, hue3 + 31) and hue2 in range(hue3 - 31, hue3 + 31)):
			print("Analogous Colors")
			return True
		else:
			return False
	else:
		color1 = colors[0]
		color2 = colors[1]
		color3 = colors[2]
		color4 = colors[3]
		hue1 = convert_to_angle(color1[0])
		hue2 = convert_to_angle(color2[0])
		hue3 = convert_to_angle(color3[0])
		hue4 = convert_to_angle(color4[0])
		if(hue2 in range(hue1 - 31, hue1 + 31) and hue3 in range(hue1 - 31, hue1 + 31) and hue4 in range(hue1 - 31, hue1 + 31)):
			print("Analogous Colors")
			return True
		elif(hue1 in range(hue2 - 31, hue2 + 31) and hue3 in range(hue2 - 31, hue2 + 31) and hue4 in range(hue2 - 31, hue2 + 31)):
			print("Analogous Colors")
			return True
		elif(hue1 in range(hue3 - 31, hue3 + 31) and hue2 in range(hue3 - 31, hue3 + 31) and hue4 in range(hue3 - 31, hue3 + 31)):
			print("Analogous Colors")
			return True
		elif(hue1 in range(hue4 - 31, hue4 + 31) and hue2 in range(hue4 - 31, hue4 + 31) and hue3 in range(hue4 - 31, hue4 + 31)):
			print("Analogous Colors")
			return True
		else:
			return False
def triadic_colors(color1, color2, color3): # https://www.sessions.edu/color-calculator/ # https://dev.to/madsstoumann/colors-are-math-how-they-match-and-how-to-build-a-color-picker-4ei8
	hue1 = convert_to_angle(color1[0])
	hue2 = convert_to_angle(color2[0])
	hue3 = convert_to_angle(color3[0])
	if hue2 in range(hue1 + 100, hue1 + 140) and hue3 in range(hue1 - 140, hue1 - 100):
		print("Triadic Colors")
		return True
	elif hue3 in range(hue1 + 100, hue1 + 140) and hue2 in range(hue1 - 140, hue1 - 100):
		print("Triadic Colors")
		return True
	elif hue1 in range(hue2 + 100, hue2 + 140) and hue3 in range(hue2 - 140, hue2 - 100):
		print("Triadic Colors")
		return True
	elif hue3 in range(hue2 + 100, hue2 + 140) and hue1 in range(hue2 - 140, hue2 - 100):
		print("Triadic Colors")
		return True
	elif hue1 in range(hue3 + 100, hue3 + 140) and hue2 in range(hue3 - 140, hue3 - 100):
		print("Triadic Colors")
		return True
	elif hue2 in range(hue3 + 100, hue3 + 140) and hue1 in range(hue3 - 140, hue3 - 100):
		print("Triadic Colors")
		return True
	else:
		return False
def square_colors(color1, color2, color3, color4): # https://www.sessions.edu/color-calculator/ # https://dev.to/madsstoumann/colors-are-math-how-they-match-and-how-to-build-a-color-picker-4ei8
	hues = sorted([convert_to_angle(color1[0]), convert_to_angle(color2[0]), convert_to_angle(color3[0]), convert_to_angle(color4[0])])
	hue1 = convert_to_angle(hues[0])
	hue2 = convert_to_angle(hues[1])
	hue3 = convert_to_angle(hues[2])
	hue4 = convert_to_angle(hues[3])
	if hue2 in range(hue1 + 70, hue1 + 110) and hue3 in range(hue1 + 160, hue1 + 200) and hue4 in range(hue1 + 250, hue1 + 290):
		print("Square Colors")
		return True
	else:
		return False
def tetradic_rectangle(color1, color2, color3, color4): # https://www.sessions.edu/color-calculator/ # https://dev.to/madsstoumann/colors-are-math-how-they-match-and-how-to-build-a-color-picker-4ei8
	hues = sorted([convert_to_angle(color1[0]), convert_to_angle(color2[0]), convert_to_angle(color3[0]), convert_to_angle(color4[0])])
	hue1 = convert_to_angle(hues[0])
	hue2 = convert_to_angle(hues[1])
	hue3 = convert_to_angle(hues[2])
	hue4 = convert_to_angle(hues[3])
	if hue2 in range(hue1 + 40, hue1 + 80) and hue3 in range(hue1 + 160, hue1 + 200) and hue4 in range(hue1 + 220, hue1 + 260):
		print("Tetradic Rectangle Colors")
		return True
	else:
		return False
def tints(colors): # https://dev.to/madsstoumann/colors-are-math-how-they-match-and-how-to-build-a-color-picker-4ei8
	for i in range(len(colors)):
		for j in range(len(colors)):
			if colors[i][0] != colors[j][0] and colors[i][0] != colors[j][0] + 1 and colors[i][0] != colors[j][0] - 1:
				return False
			if colors[i][1] != colors[j][1] and colors[i][1] != colors[j][1] + 1 and colors[i][1] != colors[j][1] - 1:
				return False
	print("Tints")
	return True
def generate_complementary(color):
	return [255 - color[0], 255 - color[1], 255 - color[2]]
def suggest_colors(list_of_colors):
    red = [255, 0, 0, 'red']
    blue = [0, 0, 255, 'blue']
    green = [0, 255, 0, 'green']
    yellow = [255, 255, 0, 'yellow']
    purple = [255, 0, 255, 'purple']
    aqua = [0, 255, 255, 'aqua']
    orange = [255, 162, 0, 'orange']
    pink = [255, 145, 223, 'pink']
    colors = [red, blue, green, yellow, purple, aqua, orange, pink]
    min_val = 1000000
    min_color = ""
    if len(list_of_colors) == 1:
        recommended_color = closest_color(generate_complementary(list_of_colors[0]))
        return "Try " + str(recommended_color[3]) + " with your current color"
    if len(list_of_colors) == 2:
        recommended_color1 = closest_color(generate_complementary(list_of_colors[0]))
        recommended_color2 = closest_color(generate_complementary(list_of_colors[1]))
        return "Try " + str(recommended_color1[3]) + " instead of " + str(closest_color(list_of_colors[1])[3]) + " or " + str(recommended_color2[3]) + " instead of " + str(closest_color(list_of_colors[0])[3])
def color_theory(listOfColors):
	listOfHSLColors = []
	for i in listOfColors:
		if(len(i) > 6):
			print("Invalid hex code detected, aborting")
			return False
		listOfHSLColors.insert(0, rgb_to_hsl(i)) # https://docs.python.org/3/tutorial/datastructures.html
	#print("HSL Values:")
	#print(listOfHSLColors)
	if len(listOfHSLColors) < 2:
		print("Need more than 2 colors")
		return False
	elif len(listOfHSLColors) == 2:
		if([0, 0, 0] in listOfColors or [255, 255, 255] in listOfColors):
			print("Everything goes with black and white")
			return True
		return (complementary(listOfHSLColors[0], listOfHSLColors[1]) or analogous_colors(listOfHSLColors) or tints(listOfHSLColors))
	elif len(listOfHSLColors) == 3:
		#print("here")
		return (triadic_colors(listOfHSLColors[0], listOfHSLColors[1], listOfHSLColors[2]) or split_complementary(listOfHSLColors[0], listOfHSLColors[1], listOfHSLColors[2]) or analogous_colors(listOfHSLColors) or tints(listOfHSLColors))
	elif len(listOfHSLColors) == 4:
		return (square_colors(listOfHSLColors[0], listOfHSLColors[1], listOfHSLColors[2], listOfHSLColors[3]) or tetradic_rectangle(listOfHSLColors[0], listOfHSLColors[1], listOfHSLColors[2], listOfHSLColors[3]) or analogous_colors(listOfHSLColors)  or tints(listOfHSLColors))
	else:
		return (analogous_colors(listOfHSLColors) or tints(listOfHSLColors))
#Tests
# print("-------")
# print("Aqua and Red")
# print("RGB Values: [255, 0, 0] - Red and [0, 255, 255] - Aqua")
# print(color_theory([[255, 0, 0], [0, 255, 255]]))
# print("-------")
# print("-------")
# print("Red and Light Red")
# print("RGB Values: [255, 0, 0] - Red and [255, 145, 145] - Light Red")
# print(color_theory([[255, 0, 0], [255, 145, 145]]))
# print("-------")
# print("Orange, Yellow, and Red")
# print("RGB Values: [255, 179, 0] - Orange, [255, 255, 0] - Yellow, [255, 0, 0] - Red")
# print(color_theory([[255, 0, 0], [255, 255, 0], [255, 0, 0]]))
# print("-------")
# print("Orange, Green, and Leaf Green")
# print("RGB Values: [255, 171, 0] - Orange, [255, 0, 171] - Fuschia, [0, 255, 174] - Leaf Green")
# print(color_theory([[255, 171, 0], [213, 0, 255], [0, 81, 255]]))
# print("-------")