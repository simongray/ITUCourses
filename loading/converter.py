__author__ = 'Anders'


def convert_line_of_studies(studies):
    if studies == 'Master i it organisation og implementering (ori)':               return 1
    if studies == 'cand.it. softwareudvikling og -teknologi (sdt)':                 return 2
    if studies == 'cand.it. e-business (ebuss)':                                    return 3
    if studies == 'Master i it interaktionsdesign og multimedier (inm)':            return 4
    if studies == 'cand.it. digital design og kommunikation (ddk)':                 return 5
    if studies == 'Master i it it-ledelse og strategi (ils)':                       return 6
    if studies == 'Bachelor i global virksomhedsinformatik (bgbi)':                 return 7
    if studies == 'Bachelor i softwareudvikling (bswu)':                            return 8
    if studies == 'Bachelor i digitale medier og design (bdmd)':                    return 9
    if studies == 'cand.it. medieteknologi og spil (mtg)':                          return 10
    if studies == 'Master i it softwarekonstruktion (sok)':                         return 11
    if studies == 'cand.it. spil (games)':                                          return 12
    if studies == 'Master i It-ledelse (ilm)':                                      return 13
    if studies == 'Master i it Interaktionsdesign (ind)':                           return 14
    if studies == 'Master i it Softwarekonstruktion (sko)':                         return 15
    if studies == 'cand.it. Digital Innovation & Management (dim)':                 return 16
    if studies == 'cand.it. design kommunikation og medier (dkm)':                  return 17
    if studies == 'cand.it. softwareudvikling (swu)':                               return 18
    if studies == 'cand.it. tværfaglig it-udvikling (tit)':                         return 19
    if studies == 'Master i it softwareudvikling (profil it-ledelse) (swu_itl)':    return 20
    if studies == 'cand.it. internet- og softwareteknologi (int)':                  return 21
    if studies == 'cand.it. it til organisationer (ito)':                           return 22
    if studies == 'Master i sundheds-it (sit)':                                     return 23


def convert_semester(semester):
    if "Efterår" in semester: return 0
    if "Forår" in semester: return 1


def convert_language(lang):
    return 0 if lang == 'Dansk' else 1


def convert_ects(ects):
    if ects == 1500:
        return 0
    else:
        return 1

def normalise(entry, max, min):
    return (entry - min)/(max - min)


def java_string_hashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000


if __name__ == '__main__':
    print()


def convert_time_slots(time_slots):
    if len(time_slots) == 0:
        return 0

    s = 0.0
    for slot in time_slots:
        time = slot["time_slot"][0:3]
        s += float(time.replace('.', ''))

    avg = s/len(time_slots)

    if avg < 10:
        return 0
    elif avg > 16:
        return 2
    else:
        return 1