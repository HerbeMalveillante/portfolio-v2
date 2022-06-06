# Here is what the compiler should do :
# - Read from the blog folder.
# - Each .md file in the blog folder is a post.
# - For each post, create a .html file in the 'blog/compiled' folder, with the correct headers and footers, and the content of the post.
# - Update the projects.html file to display the new posts.
#
# Supported Markdown syntax :
# - Headers :
#   - # Title -> h1
#   - ## Title -> h2
#   - ### Title -> h3
#   - #### Title -> h4
# - Text : 
#   - Paragraphs -> p


import os
from bs4 import BeautifulSoup

css = {
    'h1': 'text-2xl font-bold mb-4',
    'h2': 'text-xl font-bold text-red-400 pt-2',
    'h3': 'text-lg font-bold text-red-400 pt-2',
    'h4': 'text-sm font-bold text-red-400 pt-2',
    'date': 'text-md text-gray-300',
}

def read_files_in_blog():
    """Return a list of .md files in the blog folder"""
    return [f for f in os.listdir('blog') if f.endswith('.md')]


def extract_content(md_file):
    """
    Extract the content of the md file.

    The first # tag of the file is the title of the article.
    The first paragraph is the date of the article
    The second paragraph is the description of the article.

    Next up, everything is considered content.

    The function should return a dictionary with the following fields : 

        - title : The title of the article
        - date : The date of the article
        - description : The description of the article
        - content : a list containing tuples : For each tuple, the first element is the type of content (text, image, video, etc), and the second element is the content itself.
    """

    with open('blog/'+md_file, 'r') as f:
        text = f.read()
        # print(text)
        text_parsed = []
        currentLine = ""
        for line in text.split('\n'):

            # detect if the line contains text surrounded by a pair of asterisks.
            # if it does, replace the first one by a <strong> tag, and the second one by a </strong> tag.
            while line.find('**') != -1:
                line = line.replace('**', '<strong>', 1)
                line = line.replace('**', '</strong>', 1)
            
            # detect if the line contains text surrounded by a pair of underscores.
            # if it does, replace the first one by a <u> tag, and the second one by a </em> tag.
            while line.find('__') != -1:
                line = line.replace('__', '<u>', 1)
                line = line.replace('__', '</u>', 1)
            
            # detect if the line contains text surrounded by a pair of dashes.
            # if it does, replace the first one by a <del> tag, and the second one by a </del> tag.
            while line.find('--') != -1:
                line = line.replace('--', '<del>', 1)
                line = line.replace('--', '</del>', 1)
            
            # detect if the line contains text surrounded by underscores,
            # and if it does, replace the first one by a <em> tag, and the second one by a </em> tag.
            while line.find('_') != -1:
                line = line.replace('_', '<em>', 1)
                line = line.replace('_', '</em>', 1)
            
            # detect if the line contains text surrounded by single asterisks.
            # if it does, replace the first one by a <em> tag, and the second one by a </em> tag.
            while line.find('*') != -1:
                line = line.replace('*', '<em>', 1)
                line = line.replace('*', '</em>', 1)


            if line.startswith('#'):
                if currentLine != "":
                    text_parsed.append(currentLine.strip())
                else : 
                    currentLine = line
            
            elif line == "":
                if currentLine != "":
                    text_parsed.append(currentLine.strip())
                currentLine = ""
            
            else :
                currentLine += " " + line.strip()


        # store the three first elements in a separate list
        title = text_parsed[0].replace('#', '').strip()
        date = text_parsed[1].strip()
        description = text_parsed[2].strip()

        # store the rest of the elements in a list of tuples
        content = []
        for line in text_parsed[3:]:
            if line.startswith('####'):
                content.append(('h4', line.replace('####', '').strip()))
            elif line.startswith('###'):
                content.append(('h3', line.replace('###', '').strip()))
            elif line.startswith('##'):
                content.append(('h2', line.replace('##', '').strip()))
            else :
                content.append(('p', line.strip()))

        return {'filename':md_file.split('.')[0],'title': title, 'date': date, 'description': description, 'content': content}


def create_html_from_md(md_content):
    """
    Converts the md file into an html file. Returns the html file as a string.

    To do so : A file named 'article_template.html' exists in the root folder.
    """

    soup = BeautifulSoup(open('article_template.html'), 'html.parser')

    title = soup.title
    # print(title)
    title_to_change = soup.find('title')
    title_to_change.string.replace_with(md_content["title"])


    # find the tag with the id 'content'
    content = soup.find('div', id='content')

    semi_header = soup.new_tag('div', attrs={'class':'flex items-center justify-between mb-5'})
    tag_title = soup.new_tag('h1', attrs={'class':css['h1']})
    tag_title.string = md_content["title"]
    semi_header.append(tag_title)
    tag_date = soup.new_tag('h2', attrs={'class':css['date']})
    tag_date.string = md_content["date"]
    semi_header.append(tag_date)
    content.append(semi_header)

    # add the description
    tag_description = soup.new_tag('p', attrs={'class':'text-lg'})
    tag_description.string = md_content["description"]
    content.append(tag_description)

    for element in md_content["content"]:
        if element[0] in css.keys():
            css_class = css[element[0]]
        else : 
            css_class = ''
        new_tag = soup.new_tag(element[0], attrs={'class':css_class})
        new_tag.string = element[1]
        content.append(new_tag)

    # print(content)

    new_file = soup.prettify()
    # save the file in the blog/compiled folder.
    with open('blog/compiled/'+md_content["filename"]+'.html', 'w') as f:
        f.write(new_file)
    print("Created file : blog/compiled/"+md_content["filename"]+".html")

for md_file in read_files_in_blog():
    # create_html_from_md(md_file)
    content = extract_content(md_file)
    create_html_from_md(content)
