#Andrew Dallas
#Financial Cadence
#Plays a unique song which provides an aural indication of the stock performance of the given company.
import urllib.request
import pyaudio
import numpy as np
import math


#Features: 
#	Key based on first letter of stock symbol
#	Overall trend is down -> key is minor
#	Overall trend up -> key is major
#	Day to day change is negative -> moves to minor chord
#	Day to day change is positive -> moves to major chord
#	Larger changes typically result in stronger progressions, i.e. movement by fifths and fourths vs. seconds and thirds or to diminshed vs minor seconds and thirds
#	Volume is proportional to the relative trading volume of the day
#	Can change how much data you want to hear with length parameter
#	Can change temp with quarter note parameter


p = pyaudio.PyAudio()
volume = 0.5     
fs = 44100       
base_url = "http://ichart.finance.yahoo.com/table.csv?s="
root_note = 440.0
quarter_note = 1.0
length = 10


def major_chord(root,duration):
	samples = (np.sin(2*np.pi*np.arange(fs*duration)*root/fs)).astype(np.float32)
	samples2 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(4.0/12.0)/fs)).astype(np.float32)
	samples3 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(7.0/12.0)/fs)).astype(np.float32)
	samples4 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(12.0/12.0)/fs)).astype(np.float32)
	return samples + 0.5*samples2 + 0.25*samples3 + 0.25*samples4

def minor_chord(root,duration):
	samples = (np.sin(2*np.pi*np.arange(fs*duration)*root/fs)).astype(np.float32)
	samples2 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(3.0/12.0)/fs)).astype(np.float32)
	samples3 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(7.0/12.0)/fs)).astype(np.float32)
	samples4 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(12.0/12.0)/fs)).astype(np.float32)
	return samples + 0.5*samples2 + 0.25*samples3 + 0.25*samples4


def min7_chord(root,duration):
	samples = (np.sin(2*np.pi*np.arange(fs*duration)*root/fs)).astype(np.float32)
	samples2 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(3.0/12.0)/fs)).astype(np.float32)
	samples3 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(7.0/12.0)/fs)).astype(np.float32)
	samples4 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(10.0/12.0)/fs)).astype(np.float32)
	return samples + 0.25*samples2 + 0.25*samples3 + 0.5*samples4


def leading7_chord(root,duration):
	samples = (np.sin(2*np.pi*np.arange(fs*duration)*root/fs)).astype(np.float32)
	samples2 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(4.0/12.0)/fs)).astype(np.float32)
	samples3 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(7.0/12.0)/fs)).astype(np.float32)
	samples4 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(11.0/12.0)/fs)).astype(np.float32)
	return samples + 0.25*samples2 + 0.25*samples3 + 0.5*samples4

def augmented6_chord(root,duration):
	samples = (np.sin(2*np.pi*np.arange(fs*duration)*root/fs)).astype(np.float32)
	samples2 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(4.0/12.0)/fs)).astype(np.float32)
	samples3 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(7.0/12.0)/fs)).astype(np.float32)
	samples4 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(9.0/12.0)/fs)).astype(np.float32)
	return samples + 0.25*samples2 + 0.25*samples3 + 0.5*samples4

def diminished_chord(root,duration):
	samples = (np.sin(2*np.pi*np.arange(fs*duration)*root/fs)).astype(np.float32)
	samples2 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(3.0/12.0)/fs)).astype(np.float32)
	samples3 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(6.0/12.0)/fs)).astype(np.float32)
	samples4 = (np.sin(2*np.pi*np.arange(fs*duration)*root*2.0**(12.0/12.0)/fs)).astype(np.float32)
	return samples + 0.25*samples2 + 0.5*samples3 + 0.25*samples4


def single_note(root,duration):
	samples = (np.sin(2*np.pi*np.arange(fs*duration)*root/fs)).astype(np.float32)
	return samples 

def make_url(ticker_symbol):
    return base_url + ticker_symbol

def pull_historical_data(ticker_symbol, directory="S&P"):
	data = urllib.request.urlopen(make_url(ticker_symbol)) 
	i = 0
	price = []
	vol = []
	for line in data: 
		print(line.decode('utf8').split(","))
		i += 1
		if i > 1:
			price.append(float(line.decode('utf8').split(",")[4]))
			vol.append(int(line.decode('utf8').split(",")[5]))
		if i > length:
			break
	print(price)
	return price,vol


stock_ticker = "A"
while(True):
	stock_ticker = input("Enter a stock ticker:")
	price,vol = pull_historical_data(stock_ticker)

	rest_note = single_note(0,0.25)

	if(stock_ticker[0] == "A"):
		root_note = 440.0
	if(stock_ticker[0] == "B"):
		root_note = 440.0*2.0**(2.0/12.0)
	if(stock_ticker[0] == "C"):
		root_note = 440.0*2.0**(3.0/12.0)
	if(stock_ticker[0] == "D"):
		root_note = 440.0*2.0**(5.0/12.0)
	if(stock_ticker[0] == "E"):
		root_note = 440.0*2.0**(7.0/12.0)
	if(stock_ticker[0] == "F"):
		root_note = 440.0*2.0**(8.0/12.0)
	if(stock_ticker[0] == "G"):
		root_note = 440.0*2.0**(10.0/12.0)

	if(stock_ticker[0] == "H"):
		root_note = 440.0
	if(stock_ticker[0] == "I"):
		root_note = 440.0*2.0**(2.0/12.0)
	if(stock_ticker[0] == "J"):
		root_note = 440.0*2.0**(3.0/12.0)
	if(stock_ticker[0] == "K"):
		root_note = 440.0*2.0**(5.0/12.0)
	if(stock_ticker[0] == "L"):
		root_note = 440.0*2.0**(7.0/12.0)
	if(stock_ticker[0] == "M"):
		root_note = 440.0*2.0**(8.0/12.0)
	if(stock_ticker[0] == "N"):
		root_note = 440.0*2.0**(10.0/12.0)

	if(stock_ticker[0] == "O"):
		root_note = 440.0
	if(stock_ticker[0] == "P"):
		root_note = 440.0*2.0**(2.0/12.0)
	if(stock_ticker[0] == "Q"):
		root_note = 440.0*2.0**(3.0/12.0)
	if(stock_ticker[0] == "R"):
		root_note = 440.0*2.0**(5.0/12.0)
	if(stock_ticker[0] == "S"):
		root_note = 440.0*2.0**(7.0/12.0)
	if(stock_ticker[0] == "T"):
		root_note = 440.0*2.0**(8.0/12.0)
	if(stock_ticker[0] == "U"):
		root_note = 440.0*2.0**(10.0/12.0)

	if(stock_ticker[0] == "V"):
		root_note = 440.0
	if(stock_ticker[0] == "W"):
		root_note = 440.0*2.0**(2.0/12.0)
	if(stock_ticker[0] == "X"):
		root_note = 440.0*2.0**(3.0/12.0)
	if(stock_ticker[0] == "Y"):
		root_note = 440.0*2.0**(5.0/12.0)
	if(stock_ticker[0] == "Z"):
		root_note = 440.0*2.0**(7.0/12.0)

	if price[0] > 200:
		root_note *= 2

	if price[0]  < 50:
		root_note /= 2

	avgVol = 0
	for x in range(len(vol)):
		avgVol += (vol[x])
	avgVol /= 0.2*x

	stream = p.open(format=pyaudio.paFloat32,
	                channels=1,
	                rate=fs,
	                output=True)

	location = 0.0
	if(price[length-1]-price[0] >= 0):
		volume = vol[0]/avgVol
		stream.write(volume*major_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
		stream.write(volume*rest_note)
		print("I")

		for x in range(1,length-2):
			volume = vol[x]/avgVol
			if ((price[x] - price[x-1])/price[x] > 4):
				if (location%12 == 0):
					location = 7
				elif (location%12 == 2):
					location = 7
				elif(location%12 == 4):
					location = 7
				elif(location%12 == 5):
					location = 12
				elif(location%12 == 7):
					location = 12
				elif(location%12 == 9):
					location = 12
				elif(location%12 == 11):
					location = 12
			elif ((price[x] - price[x-1])/price[x] >= 0):
				if (location%12 == 0):
					location = 5
				elif (location%12 == 2):
					location = 5
				elif(location%12 == 4):
					location = 5
				elif(location%12 == 5):
					location = 0
				elif(location%12 == 7):
					location = 7
				elif(location%12 == 9):
					location = 5
				elif(location%12 == 11):
					location = 7
			elif ((price[x] - price[x-1])/price[x] < -5):
				if (location%12 == 0):
					location = 9
				elif (location%12 == 2):
					location = 4
				elif(location%12 == 4):
					location = 9
				elif(location%12 == 5):
					location = 2
				elif(location%12 == 7):
					location = 11
				elif(location%12 == 9):
					location = 2
				elif(location%12 == 11):
					location = 11
			elif ((price[x] - price[x-1])/price[x] < 0):
				if (location%12 == 0):
					location = 2
				elif (location%12 == 2):
					location = 4
				elif(location%12 == 4):
					location = 5
				elif(location%12 == 5):
					location = 2
				elif(location%12 == 7):
					location = 11
				elif(location%12 == 9):
					location = 11
				elif(location%12 == 11):
					location = 4
			if (location%12 == 0):
				stream.write(volume*major_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("I")
			elif (location%12 == 2):
				stream.write(volume*minor_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("ii")
					
			elif(location%12 == 4):
				stream.write(volume*minor_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("iii")
			elif(location%12 == 5):
				stream.write(volume*major_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("IV")
		
			elif(location%12 == 7):
				stream.write(volume*major_chord(root_note*2.0**(location/12.0),2.0*quarter_note))	
				print("V")
		
			elif(location%12 == 9):
				stream.write(volume*minor_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("vi")
		
			elif(location%12 == 11):
				stream.write(volume*diminished_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("vii diminished")
		
			stream.write(volume*rest_note)

		volume = vol[length-2]/avgVol
		if(price[length-2] - price[length-3] > 0):

			stream.write(volume*major_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
			stream.write(volume*rest_note)
			print("V")
		
		else:
			stream.write(volume*diminished_chord(root_note*2.0**(5.0/12.0),2.0*quarter_note))
			stream.write(volume*rest_note)
			print("vii diminished")
		
			stream.write(volume*single_note(root_note/2*2**(11.0/12.0),4.0*quarter_note))
			stream.write(volume*rest_note)
			stream.write(volume*single_note(root_note/2*2**(11.0/12.0),0.5*quarter_note))
		volume = vol[length-1]/avgVol
		print("I")
		
		stream.write(volume*major_chord(root_note,8.0*quarter_note))
	else:
		volume = vol[0]/avgVol
		print("i")
		# print(price[0])
		stream.write(volume*minor_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
		stream.write(volume*rest_note)

		for x in range(1,length-2):
			# print(price[x])
			volume = vol[x]/avgVol
			if ((price[x] - price[x-1])/price[x] > 4):
				if (location%12 == 0):
					location = 7
				elif (location%12 == 2):
					location = 7
				elif(location%12 == 3):
					location = 8
				elif(location%12 == 5):
					location = 0
				elif(location%12 == 7):
					location = 0
				elif(location%12 == 8):
					location = 7
				elif(location%12 == 11):
					location = 12
			elif ((price[x] - price[x-1])/price[x] >= 0):
				if (location%12 == 0):
					location = 8
				elif (location%12 == 2):
					location = 8
				elif(location%12 == 3):
					location = 0
				elif(location%12 == 5):
					location = 7
				elif(location%12 == 7):
					location = 3
				elif(location%12 == 8):
					location = 3
				elif(location%12 == 11):
					location = 0
			elif ((price[x] - price[x-1])/price[x] < -5):
				if (location%12 == 0):
					location = 2
				elif (location%12 == 2):
					location = 11
				elif(location%12 == 3):
					location = 5
				elif(location%12 == 5):
					location = 2
				elif(location%12 == 7):
					location = 11
				elif(location%12 == 8):
					location = 11
				elif(location%12 == 11):
					location = 11
			else:
				if (location%12 == 0):
					location = 2
				elif (location%12 == 2):
					location = 11
				elif(location%12 == 3):
					location = 2
				elif(location%12 == 5):
					location = 11
				elif(location%12 == 7):
					location = 2
				elif(location%12 == 8):
					location = 5
				elif(location%12 == 11):
					location = 2

			if (location%12 == 0):
				stream.write(volume*minor_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("i")
		
			elif (location%12 == 2):
				stream.write(volume*diminished_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("ii diminished")
		
			elif(location%12 == 3):
				stream.write(volume*major_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("III")
		
			elif(location%12 == 5):
				stream.write(volume*minor_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("iv")
		
			elif(location%12 == 7):
				stream.write(volume*major_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("V")
			
			elif(location%12 == 6):
				stream.write(volume*major_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("VI")
		
			elif(location%12 == 11):
				stream.write(volume*diminished_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
				print("vii diminished")
		
			stream.write(volume*rest_note)

		volume = vol[length-2]/avgVol
		# print(price[length-2])
		if(price[length-2] - price[length-3] > 0):
			print("V")
			stream.write(volume*major_chord(root_note*2.0**(location/12.0),2.0*quarter_note))
			stream.write(volume*rest_note)
			stream.write(volume*single_note(root_note/2*2**(11.0/12.0),0.5*quarter_note))
		else:
			stream.write(volume*diminished_chord(root_note*2.0**(5.0/12.0),2.0*quarter_note))
			stream.write(volume*rest_note)
			print("vii diminished")
			stream.write(volume*single_note(root_note/2*2**(11.0/12.0),4.0*quarter_note))
			stream.write(volume*rest_note)
			stream.write(volume*single_note(root_note/2*2**(11.0/12.0),0.5*quarter_note))
		print("i")
		# print(price[length-1])
		volume = vol[length-1]/avgVol
		stream.write(volume*minor_chord(root_note,8.0*quarter_note))




stream.stop_stream()
stream.close()

p.terminate()
