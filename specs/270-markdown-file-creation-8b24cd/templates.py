"""
Template pool for deterministic content generation in feature 270.

This module provides a curated collection of title+prose pairs for markdown file creation.
Each template is pre-validated to produce a 400-600 byte markdown file when formatted with
the structure: "# Title\n\nProse\n"

Templates are organized by topic for readability and maintainability.
"""


# Technology & Software Development (8 templates)
# Topics: development practices, testing, collaboration, optimization
TEMPLATES = [
    {
        "title": "The Power of Testing",
        "prose": "Comprehensive testing is the foundation of reliable software systems, ensuring that code behaves correctly under a wide variety of conditions and edge cases. By validating both happy paths and error scenarios, we build confidence that our systems will perform reliably when deployed to production. Investing in thorough test coverage today prevents costly failures and enables teams to iterate with confidence.",
    },
    {
        "title": "Mastering Code Refactoring",
        "prose": "Refactoring is the art of improving code without changing its external behavior, making systems more maintainable and performant. When done systematically with comprehensive tests backing every change, refactoring reduces technical debt and improves developer experience. Well-refactored code becomes easier to understand, modify, and extend, enabling teams to move faster while reducing the risk of introducing bugs.",
    },
    {
        "title": "The Value of Documentation",
        "prose": "Documentation serves as the bridge between code intent and developer understanding, allowing teams to share knowledge across time and space. Clear, well-maintained documentation accelerates onboarding, reduces cognitive load for future maintainers, and prevents misunderstandings. Documentation is not just written for others but for your future self, making it an invaluable investment in long-term project success.",
    },
    {
        "title": "Debugging as Problem Solving",
        "prose": "Debugging is not merely about finding and fixing bugs but developing a methodical approach to understanding complex systems. Effective debuggers approach problems systematically, forming hypotheses and testing them with precision and patience. The skills developed through deliberate debugging practice translate directly into better software architecture and design decisions.",
    },
    {
        "title": "API Design Principles",
        "prose": "Well-designed APIs are the foundation of scalable, maintainable systems, providing clear contracts between components. Thoughtful API design considers not just current needs but future extensibility, making minimal assumptions about how consumers will use interfaces. APIs that follow consistent naming conventions and predictable patterns reduce cognitive load and enable developers to work more effectively.",
    },
    {
        "title": "The Science of Optimization",
        "prose": "Optimization requires measuring before optimizing, understanding bottlenecks, and making informed decisions based on data. Premature optimization leads to complex code that sacrifices readability for unproven performance gains. The best approach is to write clear, straightforward code first, then measure and optimize only the parts that genuinely impact system performance.",
    },
    {
        "title": "Version Control Best Practices",
        "prose": "Version control is the backbone of collaborative development, tracking changes and enabling teams to work on parallel features. Meaningful commit messages and logical changesets make history readable and enable developers to understand why decisions were made. A disciplined approach to version control creates a clear audit trail and facilitates collaboration across large teams.",
    },
    {
        "title": "Continuous Integration Benefits",
        "prose": "Continuous integration catches integration problems early, preventing the accumulation of conflicting changes that become exponentially harder to resolve. By running automated tests on every commit, teams gain rapid feedback on code quality and can confidently deploy changes. The discipline of CI encourages smaller, more focused commits and reduces the risk of catastrophic failures.",
    },
    # Personal Development & Philosophy (8 templates)
    # Topics: persistence, growth, learning, resilience, collaboration
    {
        "title": "The Power of Persistence",
        "prose": "Persistence is the key to achieving meaningful goals, transforming challenges into opportunities for growth and learning through dedicated effort. When we persist through difficulties, we develop resilience and discover capabilities we never knew we possessed, expanding our sense of what is possible. The most successful people often attribute their achievements not to innate talent but to consistent effort, patience, and unwavering determination to improve incrementally over time.",
    },
    {
        "title": "Embracing Continuous Learning",
        "prose": "The most valuable skill in today's rapidly changing world is the ability to learn continuously and adapt to new challenges with flexibility and intellectual humility. Growth mindset recognizes that abilities are not fixed traits but rather developed through dedication, practice, and strategic effort to build mastery. Every mistake becomes a learning opportunity when approached with genuine curiosity, analytical thinking, and willingness to examine what went wrong.",
    },
    {
        "title": "The Art of Collaboration",
        "prose": "Collaboration is the cornerstone of human achievement, enabling individuals to combine their unique talents and perspectives toward common goals. Throughout history, collaborative efforts have produced breakthrough innovations, from scientific discoveries to artistic masterpieces that could not have been created by solitary individuals. When people work together effectively with clear communication, mutual respect, and shared purpose, they accomplish far more than they could achieve in isolation.",
    },
    {
        "title": "Finding Purpose in Work",
        "prose": "Work that aligns with our values and purpose provides not just financial stability but deep satisfaction and meaning that enriches our lives. When we understand how our contributions matter and impact others, we develop intrinsic motivation that sustains effort through challenges and setbacks. Purpose-driven work creates energy and engagement that external rewards alone cannot generate, leading to greater fulfillment.",
    },
    {
        "title": "The Value of Patience",
        "prose": "Patience is often underestimated in a world that celebrates speed and instant gratification, yet lasting success requires patience and strategic thinking. True patience is not passivity but disciplined persistence toward long-term goals while maintaining focus despite setbacks and temporary obstacles. The ability to wait for the right moment and endure temporary discomfort often determines who achieves meaningful success.",
    },
    {
        "title": "Building Resilience",
        "prose": "Resilience is the capacity to bounce back from adversity, not through denial but through adaptive responses to challenges and setbacks. Resilient people view setbacks as temporary and specific rather than permanent and universal, maintaining hope and agency. Building resilience requires consistent practice, strong support systems, and a genuine commitment to learning meaningful lessons from difficult experiences.",
    },
    {
        "title": "The Power of Creativity",
        "prose": "Creativity is not mystical talent reserved for the gifted but a skill developed through exposure to diverse perspectives and deliberate practice. Creative problem-solving requires combining existing ideas in novel ways and remaining open to unconventional solutions that challenge established thinking. In both art and technology, creativity drives innovation and enables us to tackle challenges in ways that seemed impossible before.",
    },
    {
        "title": "Mastering Time Management",
        "prose": "Effective time management is fundamentally about aligning daily activities with core priorities and values to achieve meaningful results. Rather than trying to do everything, successful people ruthlessly focus on high-impact activities that move them toward their most important goals. Time is the most finite resource we have, making its careful allocation one of the most important decisions we make.",
    },
    # Nature & Environment (6 templates)
    # Topics: sustainability, ecosystems, natural systems, interconnectedness
    {
        "title": "The Beauty of Ecosystems",
        "prose": "Natural ecosystems demonstrate remarkable interdependence and complexity, where each species plays a vital role in maintaining overall balance and health. When one species becomes threatened or extinct, the ripple effects cascade through entire ecological networks in ways we cannot always predict. Understanding and protecting ecosystems teaches us about resilience and the critical importance of maintaining diversity in all complex systems.",
    },
    {
        "title": "Renewable Energy Revolution",
        "prose": "The transition to renewable energy represents one of the most important challenges and opportunities facing our civilization today. Solar, wind, and hydroelectric power demonstrate conclusively that clean energy is not just environmentally responsible but increasingly economically competitive. This transformation requires continuous innovation in storage, distribution, and consumption patterns to create truly sustainable energy systems.",
    },
    {
        "title": "Ocean Conservation Matters",
        "prose": "Oceans cover most of Earth's surface and regulate climate patterns, generate oxygen, and support incredible biodiversity that we are only beginning to understand. Human activities like overfishing, plastic pollution, and climate change threaten marine ecosystems in ways that could have irreversible consequences. Protecting oceans requires unprecedented international cooperation and sustained commitment to sustainable practices.",
    },
    {
        "title": "Forest Preservation",
        "prose": "Forests are not just beautiful natural spaces for recreation and inspiration but critical carbon sinks, water regulators, and habitats for countless species. Deforestation for agriculture, development, and logging destroys ecosystems that took centuries to develop and establish. Protecting and restoring forests is absolutely essential for combating climate change and preserving biodiversity.",
    },
    {
        "title": "Climate Change Understanding",
        "prose": "Climate change represents the defining environmental challenge of our era, affecting weather patterns, sea levels, and ecosystems globally. The scientific consensus is clear that human activities, particularly greenhouse gas emissions, are driving unprecedented climate change. Addressing this challenge requires transformative changes in energy, transportation, agriculture, and consumption patterns.",
    },
    {
        "title": "Wildlife Protection",
        "prose": "Wildlife protection ensures that future generations inherit a world rich in biological diversity and natural wonders and beauty. Species extinction due to habitat loss, hunting, and environmental degradation represents an irreversible loss of genetic diversity. Conservation efforts that balance human needs with wildlife protection create more resilient and healthy ecosystems.",
    },
    # History & Culture (6 templates)
    # Topics: learning from history, cultural diversity, traditions, human progress
    {
        "title": "Learning From History",
        "prose": "History provides a rich and complex repository of human experiences, successes, and failures that offer valuable lessons for contemporary challenges. Those who study history carefully gain deep perspective on current events and understand how societies evolve and transform over generations. Repeating historical mistakes becomes less likely when we understand the patterns and forces that shaped past events.",
    },
    {
        "title": "Cultural Diversity Strength",
        "prose": "Cultural diversity enriches societies through exposure to different perspectives, artistic traditions, and unique ways of solving problems. When people from different backgrounds collaborate effectively, they bring varied approaches and insights that lead to more innovative and robust solutions. Celebrating diversity while promoting inclusion strengthens communities and significantly expands human understanding and capability.",
    },
    {
        "title": "The Power of Storytelling",
        "prose": "Storytelling has been a fundamental part of human culture for thousands of years, allowing us to share experiences, wisdom, and emotional connections across generations. Stories provide a powerful mechanism for communicating complex ideas through narrative, making abstract concepts tangible and memorable. Through effective storytelling, we create meaningful bonds with audiences and inspire them to think, feel, and act.",
    },
    {
        "title": "Human Rights Progress",
        "prose": "The advancement of human rights represents one of humanity's most important achievements, expanding freedom and dignity across populations and nations. Historical struggles for civil rights, women's rights, and workers' rights demonstrate both the resistance to change and the power of persistence. Continued progress requires vigilance against regression and commitment to extending rights to all people.",
    },
    {
        "title": "Preserving Cultural Heritage",
        "prose": "Cultural heritage encompasses the arts, languages, traditions, and knowledge systems that define communities and civilizations. As globalization spreads homogenizing influences globally, protecting cultural heritage becomes increasingly important for preserving human diversity and identity. Digital archives, education programs, and grassroots community efforts ensure that future generations can learn from and appreciate their cultural roots.",
    },
    {
        "title": "The Role of Architecture",
        "prose": "Architecture shapes how we live, work, and interact, reflecting both practical needs and cultural values of societies throughout history. Great architecture stands the test of time, continuing to inspire and serve communities long after its creation. Understanding architectural history reveals how built environments profoundly influence human behavior and community formation.",
    },
    # Science & Discovery (6 templates)
    # Topics: scientific method, medical breakthroughs, space exploration, research
    {
        "title": "The Scientific Method",
        "prose": "The scientific method provides a disciplined and systematic approach to understanding the natural world through careful observation, hypothesis generation, experimentation, and analysis. This systematic approach has led to remarkable discoveries across physics, biology, chemistry, and medicine throughout history. Science progresses not through individual genius but through the cumulative, peer-reviewed work of thousands of researchers collaborating.",
    },
    {
        "title": "Medical Breakthroughs",
        "prose": "Modern medicine has dramatically extended human lifespan and improved quality of life through vaccines, antibiotics, surgical innovations, and preventive care. Each breakthrough required years of dedicated research, extensive clinical trials, and iterative improvement. The pace of medical innovation continues to accelerate, with gene therapy and personalized medicine promising transformative treatments.",
    },
    {
        "title": "Space Exploration Wonder",
        "prose": "Space exploration pushes the boundaries of human capability and expands our understanding of the universe and our place in it. From landing on the moon to discovering thousands of exoplanets, these achievements inspire awe and drive technological innovation. The challenges of space exploration create solutions that improve life on Earth in unexpected and beneficial ways.",
    },
    {
        "title": "Quantum Physics Revolution",
        "prose": "Quantum physics revealed that reality at the smallest scales operates according to principles radically different from everyday experience and classical mechanics. This revolution in understanding has led to practical technologies like semiconductors, lasers, and quantum computers. Quantum mechanics continues to challenge our deepest intuitions while enabling new technological possibilities.",
    },
    {
        "title": "Artificial Intelligence Progress",
        "prose": "Artificial intelligence is transforming how we work, communicate, and solve problems by enabling machines to learn from data and improve over time. From medical diagnosis to scientific research, AI accelerates discovery and enables new capabilities that were previously impossible. Responsible development of AI requires careful attention to ethics, bias, and long-term societal impacts.",
    },
    {
        "title": "Genetic Research Implications",
        "prose": "Genetic research has successfully decoded the blueprint of life, revealing how heredity shapes organisms and enabling treatments for genetic diseases. CRISPR and other gene-editing technologies offer unprecedented ability to modify organisms at the molecular level. These powerful tools require careful and thoughtful ethical consideration of intended and unintended consequences.",
    },
    # Business & Economics (6 templates)
    # Topics: entrepreneurship, innovation, markets, leadership
    {
        "title": "Entrepreneurship Challenges",
        "prose": "Entrepreneurship requires far more than a good idea but demands disciplined execution, resilience through setbacks, and willingness to pivot when data suggests change. Successful entrepreneurs combine unbounded optimism with ruthless pragmatism, pursuing vision while maintaining flexibility. The journey from startup to sustainable business involves countless challenges and rich learning opportunities.",
    },
    {
        "title": "Innovation Management",
        "prose": "Organizations that innovate consistently develop unique cultures that encourage experimentation and tolerate intelligent failures as valuable learning opportunities. Innovation requires carefully balancing exploration of new ideas with exploitation of proven business models. Companies that excel at innovation create feedback loops that rapidly test ideas and scale winners.",
    },
    {
        "title": "Market Dynamics Understanding",
        "prose": "Markets are complex adaptive systems where supply, demand, competition, and innovation continuously interact to create opportunities and disruption. Understanding market dynamics helps entrepreneurs and investors identify where value can be created. Disruptive innovations often come from outside existing markets, challenging established players through innovative approaches.",
    },
    {
        "title": "Leadership Excellence",
        "prose": "Effective leaders inspire teams by articulating compelling visions, building psychological safety, and developing talent systematically throughout organizations. Great leaders recognize that their primary responsibility is enabling others to do their best work and grow. Leadership quality directly influences organizational culture, innovation, and long-term strategic success.",
    },
    {
        "title": "Sustainable Business Models",
        "prose": "Sustainable business models create value for customers, shareholders, and society while operating within environmental and social boundaries. Companies that integrate sustainability into core strategy often discover cost savings and competitive advantages. The future belongs to businesses that can operate profitably while solving rather than exacerbating environmental and social problems.",
    },
    {
        "title": "Financial Literacy Importance",
        "prose": "Financial literacy enables individuals and organizations to make informed decisions about money, investing, and long-term planning successfully. Understanding concepts like compound interest, risk management, and asset allocation creates the strong foundation for financial security. Financial education should be universal, empowering people to build wealth and achieve their goals.",
    },
]


def load_templates() -> list[dict[str, str]]:
    """
    Load and return the template pool.

    Returns:
        List of template dictionaries, each with 'title' and 'prose' keys.
    """
    return TEMPLATES


def calculate_markdown_bytes(title: str, prose: str) -> int:
    """
    Calculate the byte size of a markdown file with given title and prose.

    Args:
        title: The H1 heading text (without the '# ' prefix).
        prose: The prose paragraph content.

    Returns:
        The byte size of the formatted markdown content in UTF-8.
    """
    # Format: "# Title\n\nProse\n"
    content = f"# {title}\n\n{prose}\n"
    return len(content.encode('utf-8'))


def validate_template(template: dict[str, str]) -> tuple[bool, str | None]:
    """
    Validate a single template against requirements.

    Args:
        template: Template dict with 'title' and 'prose' keys.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not isinstance(template, dict):
        return False, "Template must be a dictionary"

    if 'title' not in template or 'prose' not in template:
        return False, "Template must have 'title' and 'prose' keys"

    title = template['title']
    prose = template['prose']

    if not isinstance(title, str) or not isinstance(prose, str):
        return False, "Title and prose must be strings"

    if len(title) < 3 or len(title) > 100:
        return False, f"Title must be 3-100 characters, got {len(title)}"

    if len(prose) < 100:
        return False, f"Prose must be at least 100 characters, got {len(prose)}"

    # Check sentence count (2-3 sentences)
    sentence_endings = sum(1 for char in prose if char in '.!?')
    if sentence_endings < 2 or sentence_endings > 3:
        return False, f"Prose must have 2-3 sentences, got {sentence_endings}"

    # Check byte size (400-600)
    byte_size = calculate_markdown_bytes(title, prose)
    if byte_size < 400 or byte_size > 600:
        return False, f"Template produces {byte_size} bytes, must be 400-600"

    return True, None


def validate_all_templates() -> tuple[bool, list[str]]:
    """
    Validate all templates in the pool.

    Returns:
        Tuple of (all_valid, list_of_errors).
    """
    errors = []
    for i, template in enumerate(TEMPLATES):
        is_valid, error = validate_template(template)
        if not is_valid:
            errors.append(f"Template {i}: {error}")

    return len(errors) == 0, errors


if __name__ == "__main__":
    # Validate all templates and print summary
    all_valid, errors = validate_all_templates()

    if all_valid:
        print(f"[OK] All {len(TEMPLATES)} templates are valid")
        for i, template in enumerate(TEMPLATES):
            size = calculate_markdown_bytes(template['title'], template['prose'])
            print(f"  {i+1:2d}. {template['title']:<40s} ({size:3d} bytes)")
    else:
        print(f"[ERROR] {len(errors)} template(s) failed validation:")
        for error in errors:
            print(f"  {error}")
