from webpage_reader import PageReader

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches"
    reader = PageReader(url)
    reader.parse_page()