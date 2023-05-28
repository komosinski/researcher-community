from tests.similarity.src.data.utils.category_dataset_link_downloader import CategoryDatasetLinkDownloader

# Example script for downloading random articles from science direct
# For now it needs both Firefox and Chrome

if __name__ == "__main__":
    # folder name - data is stored in data/raw
    scraper = CategoryDatasetLinkDownloader('categories')
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
    for i in [ 'Mathematics', 'Economics, Econometrics and Finance', 'Social Sciences']:
             # 'Immunology and Microbiology']:  # scraper.categories_list[0:2]:  # catergories to be sampled
        scraper.sample_from_category(i, 2)  # numbers of articles to be downloaded
