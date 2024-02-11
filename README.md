# online IDE

Aplikacja deployowana jest w chmurze i pozwala na dostęp i edycję w czasie rzeczywistym w przyszłości narzędzie będzie wspierane przez AI w celu szybkiego prototypowania i rozwoju aplikacji.

Rozruch:
<pre>
python3 app.py
</pre>

Aplikacja dostępna jest pod adresem
http://127.0.0.1:5005/app




---------------------------------------------------------------------------------------------------------
## TODO
<pre>
- [ ] Zadanie 1:

- [ ] Powinna być opcja do trakowania błędów, to znaczy, jak widzisz bład to stwórz za pomocą ai łatwy opis tego błedu -> przyszła automatyzacja
![Alt tekst](readme_assets/not_found_outside.png)

- [ ] @app.route('/fetch_file_content')
def fetch_file_content():
    filename = request.args.get('filename')
    logging.info(f"Fetching file content for: {filename}")

# TODO --> te foldery powinny być automatycznie wyszukiwane w procjecie i ładowane
    potential_paths = [
        os.path.join(os.getcwd(), filename),
        os.path.join(os.getcwd(), 'templates', filename),
        os.path.join(os.getcwd(), 'static', filename),
        os.path.join(os.getcwd(), 'static', 'js', filename),
        os.path.join(os.getcwd(), 'static', 'css', filename)
    ]

- [ ] przycisk "Create New File" powienien odpalić okno dialogowe wewnątrz edytora 




> Aby zaznaczyć zadanie jako wykonane, zmień `[ ]` na `[x]`.
</pre>

**SYSTEM DO TESTOWANIA, KTÓRY PROMPT JEST LEPSZY, A CO ZA TYM IDZIE MODEL**





You got a categories as fallow:
ROLE: The "ROLE" category defines the field or area in which an agent (or a person) has specialized expertise or experience. This category helps identify the primary function or domain of knowledge that the agent can contribute to.

In the future list a areas of expertise and build and update graph of expertise.

CONTEXT: The "CONTEXT" category provides the situational, environmental, or background information in which an action or communication is taking place. It helps to understand the circumstances and conditions that may influence decisions, interactions, or outcomes.

TASK: The "TASK" category outlines the specific activity, objective, or goal that needs to be accomplished. This category clarifies what needs to be done and provides a clear focus on the purpose of the action.

ERROR: The "ERROR" category pertains to the issues, bugs, and unexpected behaviors that arise during the development process. Categorizing and addressing errors systematically helps maintain code quality and ensures a more stable end product. The error category could include descriptions of the errors, their impact, and steps to reproduce them.

CODE: The "CODE" category involves descriptions and interactions of code snippets or files within the project. Each entry  include code snippets, functions, codebase etc.

PROJECT STRUCTURE: The "PROJECT STRUCTURE" category involves the overall organization of the software project. It includes how the codebase is structured into different modules, components, and directories.


Rozwiniie
It sounds like you're creating a framework for software development and programming support, and you have defined several categories within this framework. Here's an elaboration on the categories you mentioned:

1. **ROLE**: In the context of software development, the "ROLE" category could refer to the specific roles or responsibilities that individuals or teams have within a project. Common software development roles include software engineer, front-end developer, back-end developer, UI/UX designer, project manager, quality assurance engineer, and more. This category helps to define who is involved in the project and what their expertise is.

2. **CONTEXT**: The "CONTEXT" category could represent the broader environment in which the software development project is taking place. This includes factors such as the industry the project serves, the target audience or users, the existing technology stack, market trends, regulatory considerations, and other relevant external factors. Understanding the context helps guide decision-making and tailor the project to its intended purpose.

3. **TASK**: The "TASK" category involves the specific activities or assignments that need to be accomplished during the software development process. Tasks can range from coding and designing to testing, documentation, and deployment. Each task can be broken down into smaller subtasks, and they collectively form the roadmap for completing the project. Task management is crucial for project organization and progress tracking.

4. **ERROR**: The "ERROR" category pertains to the issues, bugs, and unexpected behaviors that arise during the development process. This includes runtime errors, logical flaws, security vulnerabilities, and more. Categorizing and addressing errors systematically helps maintain code quality and ensures a more stable end product. The error category could include descriptions of the errors, their impact, and steps to reproduce them.

5. **CODE**: The "CODE" category encompasses the actual programming code written for the project. This includes all the source code, configuration files, and scripts used to build and run the software. Organizing code efficiently, adhering to coding standards, and properly commenting the code are important aspects of this category.

6. **PROJECT STRUCTURE**: The "PROJECT STRUCTURE" category involves the overall organization of the software project. It includes how the codebase is structured into different modules, components, and directories. Additionally, it covers version control practices, branching strategies, and any development methodologies or frameworks being used (e.g., Agile, Scrum, GitFlow).

7 UPDATE SOLUTION - jak wyskakuje bład z którym nie daje sobie rady a rozwiązanie znajdzie się w necie dodaje tą komendę - TU wymaga zbudowania modelu, który uczy się on the fly po wpisaniu komendy - dodaje do swojej bazy danych i updatuje

Remember that these categories can intersect and influence each other. For instance, errors discovered during testing might lead to changes in code or task priorities. The framework you're developing aims to provide a structured approach to software development, enhancing collaboration, organization, and the overall quality of the end product.


CAŁY MODEL:
- Powinien skanować, dokumentacje i updaty języków żeby brać pod uwagę zmiany
- powinnismy stworzyć modele zachowania języka żeby testować wszystkie zmiany jakie zachodzą dzięki temu będziemy wiedzięć testami czy się coś zmieniło, moodel powinien to monitorować
