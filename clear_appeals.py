import requests
from time import sleep
from bs4 import BeautifulSoup


class Appeal(object):
    def __init__(self, num, keywords, date, summary):
        try:
            self.num = str(num[0]).split(": ")[1].rstrip("</a>")
            self.keywords = keywords[0].lower().lstrip(" ").rstrip(" ").replace(",", ";").replace(":", ";").split("; ")
            self.date = date[0]
            self.reasons = []
            self.summary = " .".join([str(x) for x in summary]).strip("\n\t ").replace("\n", " ").replace("\r", " ").lower().replace('<strong><span style="text-decoration: underline"></span></strong>', "")
            self.decision = self._decision_check(self.summary)
            self.parse_reasons()
        except IndexError as e:
            pass

    def __str__(self):
        return "Case: {}({})\nKey Words: {}\nSummary: {}\nDecision: {}".format(self.num, self.date,
                                                                               ", ".join([x for x in self.keywords]),
                                                                               self.summary,
                                                                               self.decision)

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(self.num, self.date, self.summary, self.decision, str(self.keywords))

    @staticmethod
    def _decision_check(s):
        s = s.lower().replace("u.s.s.", "").replace("u.s.c.", "").replace("\n", " ").replace("\t", " ").split("case no:")[0].rstrip(" ")
        if s[-1] == ".":
            s = str(s.replace("</span> .", "").split(".")[-2])
        elif not s[1] == ".":
            s = str(s.split(".")[-1])
        try:
            if "denied" in s:
                return "Denied"
            elif "adverse decision affirmed" in s \
                    or "favorable decision reversed" in s \
                    or "adverse decision sustained" in s\
                    or "adverse decision remanded" in s\
                    or "adverse decision is affirmed" in s\
                    or "adverse decision affirmed" in s\
                    or "adverse determination affirmed" in s:
                return "Denied"
            elif "granted" in s:
                return "Granted"
            elif "favorable decision affirmed" in s \
                    or "favorable decision remanded" in s\
                    or "adverse decision reversed" in s:
                return "Granted"
            else:
                return "Unknown"
        except IndexError as e:
            pass

    def parse_reasons(self):
        try:
            for r in self.keywords:
                r = r.lower()
                if "alcohol" in r or "guideline g" in r:
                    self.reasons.append("alcohol")
                elif "drug" in r or "guideline h" in r:
                    self.reasons.append("drugs")
                elif "emotional" in r:
                    self.reasons.append("emotional")
                elif "personal conduct" in r or "guideline e" in r or "guideline k" in r:
                    self.reasons.append("personal conduct")
                elif "foreign" in r or "guideline b" in r or "guideline c" in r:
                    self.reasons.append("foreign")
                elif "financial" in r or "guideline f" in r:
                    self.reasons.append("financial")
                elif "sex" in r or "guideline d" in r:
                    self.reasons.append("sexual")
                elif "information technology" in r or "guideline m" in r:
                    self.reasons.append("information technology")
                elif "mental" in r or "disorder" in r or "guideline i" in r:
                    self.reasons.append("mental")
                elif "security violations" in r:
                    self.reasons.append('security violations')
                elif "criminal conduct" in r or "guideline j" in r:
                    self.reasons.append('criminal conduct')
                elif "falsification" in r:
                    self.reasons.append('falsification')
                elif "outside activities" in r or "guideline l" in r:
                    self.reasons.append('outside activities')
        except KeyError as e:
            pass
        except AttributeError as e:
            pass

class AppealYear(object):
    def __init__(self, y):
        self.appeals = []
        self.outcomes = {"Granted": 0, "Denied": 0, "Unknown": 0}
        self.reasons = {"alcohol": 0, "drugs": 0, "emotional": 0, "personal conduct": 0, "foreign": 0, "financial": 0,
                        "sexual": 0, "information technology": 0, "mental": 0, 'security violations': 0,
                        'criminal conduct': 0, "falsification": 0, 'outside activities': 0, }
        self.reasons_outcome = {"alcohol": [0, 0], "drugs": [0, 0], "emotional": [0, 0], "personal conduct": [0, 0],
                                "foreign": [0, 0], "financial": [0, 0], "sexual": [0, 0],
                                "information technology": [0, 0], "mental": [0, 0], 'security violations': [0, 0],
                                'criminal conduct': [0, 0], "falsification": [0, 0], 'outside activities': [0, 0], }
        self.year = y
        self.total_cases = 0
        self._page = requests.get("http://www.dod.mil/dodgc/doha/industrial/{}.html".format(y))
        self.soup = BeautifulSoup(self._page.content)
        self.collect_data()
        self.parse_appeals()

    def collect_data(self):
        for e in self.soup.find_all("div"):
            if e['class'][0] == "case":
                n, k = [x.contents for x in e.find_all("div")]
                d, s = [x.contents for x in e.find_all("p")]
                try:
                    self.appeals.append(Appeal(n, k, d, s))
                except:
                    pass

    def parse_appeals(self):
        for appeal in self.appeals:
            self.total_cases += 1
            try:
                self.outcomes[appeal.decision] += 1
                for r in appeal.keywords:
                    r = r.lower()
                    if "alcohol" in r or "guideline g" in r:
                        self.reasons["alcohol"] += 1
                        self.decision_by_guideline(appeal, "alcohol")
                    elif "drug" in r or "guideline h" in r:
                        self.reasons["drugs"] += 1
                        self.decision_by_guideline(appeal, "drugs")
                    elif "emotional" in r:
                        self.reasons["emotional"] += 1
                        self.decision_by_guideline(appeal, "emotional")
                    elif "personal conduct" in r or "guideline e" in r or "guideline k" in r:
                        self.reasons["personal conduct"] += 1
                        self.decision_by_guideline(appeal, "personal conduct")
                    elif "foreign" in r or "guideline b" in r or "guideline c" in r:
                        self.reasons["foreign"] += 1
                        self.decision_by_guideline(appeal, "foreign")
                    elif "financial" in r or "guideline f" in r:
                        self.reasons["financial"] += 1
                        self.decision_by_guideline(appeal, "financial")
                    elif "sex" in r or "guideline d" in r:
                        self.reasons["sexual"] += 1
                        self.decision_by_guideline(appeal, "sexual")
                    elif "information technology" in r or "guideline m" in r:
                        self.reasons["information technology"] += 1
                        self.decision_by_guideline(appeal, "information technology")
                    elif "mental" in r or "disorder" in r or "guideline i" in r:
                        self.reasons["mental"] += 1
                        self.decision_by_guideline(appeal, "mental")
                    elif "security violations" in r:
                        self.reasons['security violations'] += 1
                        self.decision_by_guideline(appeal, 'security violations')
                    elif "criminal conduct" in r or "guideline j" in r:
                        self.reasons['criminal conduct'] += 1
                        self.decision_by_guideline(appeal, 'criminal conduct')
                    elif "falsification" in r:
                        self.reasons['falsification'] += 1
                        self.decision_by_guideline(appeal, 'falsification')
                    elif "outside activities" in r or "guideline l" in r:
                        self.reasons['outside activities'] += 1
                        self.decision_by_guideline(appeal, "outside activities")
            except KeyError as e:
                pass
            except AttributeError as e:
                pass

    def decision_by_guideline(self, ap, r):
        if ap.decision == "Granted":
            self.reasons_outcome[r][0] += 1
        elif ap.decision == "Denied":
            self.reasons_outcome[r][1] += 1

    def __str__(self):
        return "Year: {}\nDecisions: {} - {}\nReasons: {}\nOutcomes: {}\n".format(self.year, self.total_cases,
                                                                    str(self.outcomes), str(self.reasons),
                                                                    str(self.reasons_outcome))

    def __repr__(self):
        return str("{}, {}, {}, {}, {}".format(self.year, self.total_cases,
                                           str(self.outcomes), str(self.reasons), str(self.reasons_outcome)))

    def dec_out(self):
        return self.reasons_outcome

    def dump_appeals(self):
        return self.appeals

y = 1999
l = 0
t = 0
drugs = ["marijuana", "lsd", "mushroom", "lsd", "heroin", "crack cocaine", "cocaine", "ketamine", "mdma", "ecstasy", "prescription", "meth", "dmt"]
countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua & Deps", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Central African Rep", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Congo {Democratic Rep}", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland ", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea North", "Korea South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar, {Burma}", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "St Kitts & Nevis", "St Lucia", "Saint Vincent & the Grenadines", "Samoa", "San Marino", "Sao Tome & Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]
for ye in range(1999, 2015):
    h, s = 0, 0
    #print(repr(AppealYear(ye)))
    #print(AppealYear(ye).dec_out())
    appeals = AppealYear(ye).dump_appeals()
    for appeal in appeals:
        try:
            if "she" in appeal.summary.lower():
                s+=1
            elif "he" in appeal.summary.lower():
                h+=1
            t+=1
        except Exception as e:
            print(e)
    print(t, h, s)