from models import models
import math

def calculateMetalMineCost(level):
    if level <= 20:
        metal = int(80 * math.pow(1.48, level - 1))
        crystal = int(20 * math.pow(1.48, level - 1))
    elif level <= 30:
        metal = int(137424 * math.pow(1.46, level - 20))
        crystal = int(34356 * math.pow(1.46, level - 20))
    elif level <= 40:
        metal = int(6047713 * math.pow(1.445, level - 30))
        crystal = int(1511928 * math.pow(1.445, level - 30))
    elif level <= 50:
        metal = int(240032257 * math.pow(1.43, level - 40))
        crystal = int(60008064 * math.pow(1.43, level - 40))
    elif level <= 60:
        metal = int(8582819573 * math.pow(1.41, level - 50))
        crystal = int(2145704893 * math.pow(1.41, level - 50))
    elif level <= 65:
        metal = int(266576038331 * math.pow(1.39, level - 60))
        crystal = int(66644009575 * math.pow(1.39, level - 60))
    elif level <= 70:
        metal = int(1383232265343 * math.pow(1.37, level - 65))
        crystal = int(345808066295 * math.pow(1.37, level - 65))
    elif level <= 75:
        metal = int(6675717445001 * math.pow(1.35, level - 70))
        crystal = int(1668929361053 * math.pow(1.35, level - 70))
    elif level <= 80:
        metal = int(29934140242686 * math.pow(1.33, level - 75))
        crystal = int(7483535059787 * math.pow(1.33, level - 75))
    elif level <= 85:
        metal = int(124573307057205 * math.pow(1.31, level - 80))
        crystal = int(31143326760620 * math.pow(1.31, level - 80))
    elif level <= 90:
        metal = int(480597461040428 * math.pow(1.29, level - 85))
        crystal = int(120149365245905 * math.pow(1.29, level - 85))
    elif level <= 95:
        metal = int(1716840792312547 * math.pow(1.27, level - 90))
        crystal = int(429210198027402 * math.pow(1.27, level - 90))
    elif level <= 100:
        metal = int(5672162030942849 * math.pow(1.25, level - 95))
        crystal = int(1418040507568092 * math.pow(1.25, level - 95))
    elif level <= 105:
        metal = int(17310064791695706 * math.pow(1.23, level - 100))
        crystal = int(4327516197412390 * math.pow(1.23, level - 100))
    elif level <= 110:
        metal = int(48733123803662216 * math.pow(1.21, level - 105))
        crystal = int(12183280949475422 * math.pow(1.21, level - 105))
    elif level <= 115:
        metal = int(126401172422868705 * math.pow(1.19, level - 110))
        crystal = int(31600293101981844 * math.pow(1.19, level - 110))
    elif level <= 120:
        metal = int(301637900426963684 * math.pow(1.17, level - 115))
        crystal = int(75409475097827097 * math.pow(1.17, level - 115))
    else:
        metal = int(661325422283768720 * math.pow(1.15, level - 120))
        crystal = int(165331355551399084 * math.pow(1.15, level - 120))

    return models.Resources(metal, crystal, 0)


def calculateCrystalMineCost(level: int) -> models.Resources:
    if level <= 20:
        metal = int(64 * 1.48**(level - 1))
        crystal = int(32 * 1.48**(level - 1))
    elif level <= 30:
        metal = int(109939 * 1.46**(level - 20))
        crystal = int(54970 * 1.46**(level - 20))
    elif level <= 40:
        metal = int(4838170 * 1.445**(level - 30))
        crystal = int(2419085 * 1.445**(level - 30))
    elif level <= 50:
        metal = int(192025805 * 1.43**(level - 40))
        crystal = int(96012903 * 1.43**(level - 40))
    elif level <= 60:
        metal = int(6866255658 * 1.41**(level - 50))
        crystal = int(3433127829 * 1.41**(level - 50))
    elif level <= 65:
        metal = int(213260830652 * 1.39**(level - 60))
        crystal = int(106630415326 * 1.39**(level - 60))
    elif level <= 70:
        metal = int(1106585812208 * 1.37**(level - 65))
        crystal = int(553292906104 * 1.37**(level - 65))
    elif level <= 75:
        metal = int(5340573955680 * 1.35**(level - 70))
        crystal = int(2670286977840 * 1.35**(level - 70))
    elif level <= 80:
        metal = int(23947312192710 * 1.33**(level - 75))
        crystal = int(11973656096355 * 1.33**(level - 75))
    elif level <= 85:
        metal = int(99658645639776 * 1.31**(level - 80))
        crystal = int(49829322819888 * 1.31**(level - 80))
    elif level <= 90:
        metal = int(384477968809241 * 1.29**(level - 85))
        crystal = int(192238984404620 * 1.29**(level - 85))
    elif level <= 95:
        metal = int(1373472633767512 * 1.27**(level - 90))
        crystal = int(686736316883754 * 1.27**(level - 90))
    elif level <= 100:
        metal = int(4537729624481628 * 1.25**(level - 95))
        crystal = int(2268864812240807 * 1.25**(level - 95))
    elif level <= 105:
        metal = int(13848051832524499 * 1.23**(level - 100))
        crystal = int(6924025916262228 * 1.23**(level - 100))
    elif level <= 110:
        metal = int(38986499040587253 * 1.21**(level - 105))
        crystal = int(19493249520293566 * 1.21**(level - 105))
    elif level <= 115:
        metal = int(101120937932219071 * 1.19**(level - 110))
        crystal = int(50560468966109378 * 1.19**(level - 110))
    elif level <= 120:
        metal = int(241310320327071718 * 1.17**(level - 115))
        crystal = int(120655160163535483 * 1.17**(level - 115))
    else:
        metal = int(529060337795226169 * 1.15**(level - 120))
        crystal = int(264530168897612260 * 1.15**(level - 120))

    return models.Resources(metal, crystal, 0)


def calculateDeuteriumRefineryCost(level):
    if level <= 20:
        metal = int(340 * pow(1.48, level - 1))
        crystal = int(100 * pow(1.48, level - 1))
    elif level <= 30:
        metal = int(584052 * pow(1.46, level - 20))
        crystal = int(171780 * pow(1.46, level - 20))
    elif level <= 40:
        metal = int(25702778 * pow(1.445, level - 30))
        crystal = int(7559641 * pow(1.445, level - 30))
    elif level <= 50:
        metal = int(1020137091 * pow(1.43, level - 40))
        crystal = int(300040321 * pow(1.43, level - 40))
    elif level <= 60:
        metal = int(36476983184 * pow(1.41, level - 50))
        crystal = int(10728524466 * pow(1.41, level - 50))
    elif level <= 65:
        metal = int(1132948162869 * pow(1.39, level - 60))
        crystal = int(333220047906 * pow(1.39, level - 60))
    elif level <= 70:
        metal = int(5878737127512 * pow(1.37, level - 65))
        crystal = int(1729040331638 * pow(1.37, level - 65))
    elif level <= 75:
        metal = int(28371799140311 * pow(1.35, level - 70))
        crystal = int(8344646806055 * pow(1.35, level - 70))
    elif level <= 80:
        metal = int(127220096027188 * pow(1.33, level - 75))
        crystal = int(37417675302478 * pow(1.33, level - 75))
    elif level <= 85:
        metal = int(529436554975531 * pow(1.31, level - 80))
        crystal = int(155716633817847 * pow(1.31, level - 80))
    elif level <= 90:
        metal = int(2042539209353959 * pow(1.29, level - 85))
        crystal = int(600746826286418 * pow(1.29, level - 85))
    elif level <= 95:
        metal = int(7296573367085910 * pow(1.27, level - 90))
        crystal = int(2146050990340254 * pow(1.27, level - 90))
    elif level <= 100:
        metal = int(24106688630706210 * pow(1.25, level - 95))
        crystal = int(7090202538511950 * pow(1.25, level - 95))
    elif level <= 105:
        metal = int(73567775362262603 * pow(1.23, level - 100))
        crystal = int(21637580989111175 * pow(1.23, level - 100))
    elif level <= 110:
        metal = int(207115776158683397 * pow(1.21, level - 105))
        crystal = int(60916404753146307 * pow(1.21, level - 105))
    elif level <= 115:
        metal = int(537204982779344402 * pow(1.19, level - 110))
        crystal = int(158001465524873035 * pow(1.19, level - 110))
    elif level <= 120:
        metal = int(1281961076772004987 * pow(1.17, level - 115))
        crystal = int(377047375524844441 * pow(1.17, level - 115))
    else:
        metal = int(2810633044612639230 * pow(1.15, level - 120))
        crystal = int(826656777835285451 * pow(1.15, level - 120))

    return models.Resources(metal=metal, crystal=crystal, deuterium=0)

