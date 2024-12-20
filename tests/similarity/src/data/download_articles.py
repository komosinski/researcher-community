from tests.similarity.src.data.utils.random_articles_downloader import RandomArticleDownloader

# Example script for downloading random articles from science direct
# For now it needs both Firefox and Chrome

if __name__ == "__main__":
    # folder name - data is stored in data/raw
    scraper = RandomArticleDownloader('category_dataset')
    scraper.get_categories()
    print(scraper.categories_list)
    # currently, articles categories are: ['Chemical Engineering', 'Chemistry', 'Computer Science',
    # 'Earth and Planetary Sciences', 'Energy', 'Engineering', 'Materials Science', 'Mathematics',
    # 'Physics and Astronomy', 'Agricultural and Biological Sciences', 'Biochemistry,
    # Genetics and Molecular Biology', 'Environmental Science', 'Immunology and Microbiology',
    # 'Neuroscience', 'Medicine and Dentistry', 'Nursing and Health Professions', 'Pharmacology,
    # Toxicology and Pharmaceutical Science', 'Veterinary Science and Veterinary Medicine',
    # 'Arts and Humanities', 'Business, Management and Accounting', 'Decision Sciences',
    # 'Economics, Econometrics and Finance', 'Psychology', 'Social Sciences']
    for i in ['Social Sciences', 'Engineering', 'Biochemistry', 'Medicine and Dentistry', 'Pharmacology']:
        scraper.sample_from_category(i, 50)  # numbers of articles to be downloaded
