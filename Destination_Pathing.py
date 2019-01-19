import math
import libardrone


class Point(object):
    global x, y, Point
    def __init__(self, x, y):
        self.x = x
        self.y = y

def extractlist(string, separator):
    lststring = string.split(separator)
    ndx = 0
    lst = []
    for x in lststring:
        lst = lst + [float(lststring[ndx])]
        ndx += 1
    return lst

def flip(drone, currentPhi, amount_to_flip):
    # test this for phi values which gives rotation
    test = drone.navdata[0]

    phiDiff = abs(test - currentPhi)
    while phiDiff < amount_to_flip:
        drone.turn_left()
        test = drone.navdata[0]
        phiDiff = abs(test - currentPhi)
    drone.halt()
    return drone.navdata[0]

# THis function describes our current probabilities of crashing, thereore we always prioritize going straight
# WE will have the function working with thress possible crashes and three possible directions
# Outputs should be independent of direction, i.e. they result of this function should produce similar results but main function decides action based on type of direction
# 0 = Straight, 1 = LEft, 2 = Right
def define_turn_amount(prob_crash, direction,previous_flags, current_Phi):
    degrees = 0
    velocity = 0
    if direction == "S":
        # THis should turn the drone by some offset of Right or Left degrees
        if prob_crash[0] < .3:
            velocity = .2
            degrees = current_Phi + (180 * (prob_crash[2] - prob_crash[1]))
        else:
            # THis should turn the drone by some offset of Right, degrees of freedom = 36
            velocity = 0.0
            degrees = current_Phi + 10
    return degrees, velocity





def GPS_pathing(current_point, future_point, no_right,no_left, drone):
    delta_x = future_point.x - current_point.x
    delta_y = future_point.y - current_point.y

    currentPhi = drone.navdata[0]

    theta_radians = math.atan2(delta_y, delta_x)

    # now get the orientation of the drone correct

    amount_to_turn = theta_radians - currentPhi

    if amount_to_turn> amount_to_turn:
        currentPhi = flip(drone, currentPhi, amount_to_turn)

    # Now we are facing the optimal direction
    # So Now we need to move towards the future point
    return drone.navdata[0]

# WE would now move the drone forward






# -------------------------------------------------------------------------
# Vincenty Inverse geodetic computation function (Andre Verville)
# generates bearing and distance from two given points in lat lon
# Formulas from my Bachelor Degrees thesis, Laval University, 1978
# Credits: Thaddeus Vincenty, Survey Review, Vol.XXIII, No. 176, April 1975
# https://www.ngs.noaa.gov/PUBS_LIB/inverse.pdf
# -------------------------------------------------------------------------
def vincentyinverse(lat1deg, lon1deg, lat2deg, lon2deg):
    import math
    a, b = 6378137.0, 6356752.3141 # GRS80 ellipsoid, edit as required

    lat1rad = math.radians(lat1deg)
    lon1rad = math.radians(lon1deg)
    lat2rad = math.radians(lat2deg)
    lon2rad = math.radians(lon2deg)

    e2 = ((a * a) - (b * b)) / (a * a)
    sinlat1 = math.sin(lat1rad)
    coslat1 = math.cos(lat1rad)
    sinlat2 = math.sin(lat2rad)
    coslat2 = math.cos(lat2rad)

    deltalon = lon2rad - lon1rad
    N1 = a / ((1.0 - e2 * (sinlat1 * sinlat1))) ** 0.5
    M1 = (a * (1.0 - e2)) / ((1 - (e2 * sinlat1 * sinlat1)) ** 1.5)
    N2 = a / ((1.0 - e2 * (sinlat2 * sinlat2))) ** 0.5
    M2 = (a * (1.0 - e2)) / ((1 - (e2 * sinlat2 * sinlat2)) ** 1.5)
    X1 = N1 * coslat1
    Z1 = N1 * (1.0 - e2) * sinlat1
    X2 = N2 * coslat2
    Z2 = N2 * (1.0 - e2) * sinlat2
    Y = math.sin(deltalon) * X2
    temp = (N1 * coslat1) - (math.cos(deltalon) * X2)
    X = (temp * sinlat1) - ((Z1 - Z2) * coslat1)
    brg12 = math.atan2(Y, X)
    Y = math.sin(deltalon) * X1
    temp = (N2 * coslat2) - (math.cos(deltalon) * X1)
    X = ((Z2 - Z1) * coslat2) - (temp * sinlat2)
    brg21 = math.atan2(Y, X)
    X2P = math.cos(deltalon) * X2
    Y2 = math.sin(deltalon) * X2
    d12 = (((X2P - X1) * (X2P - X1)) + (Y2 * Y2) + ((Z2 - Z1) * (Z2 - Z1)))
    d12 = d12 ** 0.5
    brgb12 = (brg12 + brg21) / 2.0
    sinsqb = (math.sin(brgb12)) ** 2.0
    cossqb = (math.cos(brgb12)) ** 2.0
    Y = (N1 + N2) * (M1 + M2)
    X = (((M1 + M2) * sinsqb) + ((N1 + N2) * cossqb)) * 2.0
    RB = Y / X
    dist = d12 + ((d12 * d12 * d12) / (24.0 * RB * RB))
    brg12deg = math.degrees(brg12)
    brg21deg = math.degrees(brg21)
    if brg12deg < 0.0: brg12deg = brg12deg + 360.0  # adjust bearing (0-360)
    if brg21deg < 0.0: brg21deg = brg21deg + 360.0  # adjust bearing (0-360)
    brg21deg = (brg21deg + 180.0) % 360.0  # inverse bearing at 180 degrees
    return brg12deg, brg21deg, dist  # return 2 bearings and distance


def latitude_edit():
    R = 6378.1 #Radius of the Earth
    brng = 1.57 #Bearing is 90 degrees converted to radians.
    d = 15 #Distance in km

    #lat2  52.20444 - the lat result I'm hoping for
    #lon2  0.36056 - the long result I'm hoping for.

    lat1 = math.radians(52.20472) #Current lat point converted to radians
    lon1 = math.radians(0.14056) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    print(lat2)
    print(lon2)

# Get current GPS Point

# THen calculate the GPS coord of net .001 km in forward direction

