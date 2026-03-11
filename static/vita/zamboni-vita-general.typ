// Professional CV generated from JSONResume
// Using brilliant-cv template

#import "@preview/brilliant-cv:3.1.2": *

/// Add the title of a section
///
/// NOTE: If the language is non-Latin, the title highlight will not be sliced.
///
/// This is a copy of the function from the brilliant-cv package, but making it sticky
/// to prevent orphan headings.
///
/// - title (str): The title of the section.
/// - highlighted (bool): Whether the first n letters will be highlighted in accent color.
/// - letters (int): The number of first letters of the title to highlight.
/// - metadata (array): (optional) the metadata read from the TOML file.
/// - awesome-colors (array): (optional) the awesome colors of the CV.
/// -> content
#let cv-section(
  title,
  highlighted: true,
  letters: 3,
  metadata: none,
  // New parameter names (recommended)
  awesome-colors: none,
  // Old parameter names (deprecated, for backward compatibility)
  awesomeColors: _awesome-colors,
) = context {
  let metadata = if metadata != none { metadata } else { cv-metadata.get() }
  // Backward compatibility logic (remove this block when deprecating)
  let awesome-colors = if awesome-colors != none {
    awesome-colors
  } else {
    // TODO: Add deprecation warning in future version
    // Currently Typst doesn't have a standard warning mechanism for user functions
    awesomeColors
  }

  let lang = metadata.language
  let non-latin = _is-non-latin(lang)
  let before-section-skip = _get-layout-value(metadata, "before_section_skip", 1pt)
  let accent-color = _set-accent-color(awesome-colors, metadata)
  let highlighted-text = title.slice(0, letters)
  let normal-text = title.slice(letters)

  let section-title-style(str, color: black) = {
    text(size: 16pt, weight: "bold", fill: color, str)
  }

  v(before-section-skip)
  block(
    sticky: true,
    [#if non-latin {
      section-title-style(title, color: accent-color)
    } else {
      if highlighted {
        section-title-style(highlighted-text, color: accent-color)
        section-title-style(normal-text, color: black)
      } else {
        section-title-style(title, color: black)
      }
    }
    #h(2pt)
    #box(width: 1fr, line(stroke: 0.9pt, length: 100%))]
  )
}

    #import "@preview/pergamon:0.7.2": *

#let has-keyword(keywords, wanted) = {
  if keywords == none { false } else {
    keywords
      .split(",")
      .map(s => s.trim())
      .contains(wanted)
  }
}

#let publications-style = format-citation-numeric()
#let publications-ref-full = true
#let publications-key-list = ()
#let publications-include(reference) = {
  if publications-ref-full {
    true
  } else {
    publications-key-list.contains(reference.entry_key)
  }
}

#add-bib-resource(read("zamboni-vita-general-vita.bib"))


#let metadata = (
  language: "en",
  name: "Diego Zamboni",
  tagline: "CISO • Organizational Leader • Security Expert • Computer Scientist",

  personal: (
    first_name: "Diego",
    last_name: "Zamboni",
    info: (
      email: "diego@zzamboni.org",
      custom-homepage: (
        awesomeIcon: "home",
        text: "zzamboni.org",
        link: "https://zzamboni.org"
      ),
      location: "Zurich",
      linkedin: "zzamboni",
      custom-leanpub: (
        awesomeIcon: "leanpub",
        text: "zzamboni",
        link: "https://leanpub.com/u/zzamboni"
      ),
      github: "zzamboni",
      custom-bluesky: (
        awesomeIcon: "bluesky",
        text: "zzamboni.org",
        link: "https://bsky.app/profile/zzamboni.org"
      )
    )
  ),

  layout: (
    awesome_color: "skyblue",
    before_section_skip: "1pt",
    before_entry_skip: "1pt",
    before_entry_description_skip: "1pt",
    paper_size: "a4",
    page_margin: (x: 1.5cm, y: 1.5cm),

    header: (
      display_profile_photo: true,
      profile_photo_radius_pt: "50%",
      info_row_font_size: "8pt",
      header_align: "center"
    ),

    entry: (
      display_logo: true,
      display_entry_society_first: true,
    ),

    footer: (
      display_page_counter: true,
      display_footer: true,
    ),

    fonts: (),
  ),

  inject: (
    inject_ai_prompt: false,
    inject_keywords: false,
    injected_keywords_list: []
  ),

  lang: (
    en: (
      education: "Education",
      professional: "Professional Experience",
      certificates: "Certifications",
      skills: "Skills",
      projects: "Projects",
      activities: "Professional Activities",
      languages: "Languages",
      date_in_present: "Present",
      cv_footer: [ Curriculum Vitae - #datetime.today().display() ],
      header_quote: "CISO • Organizational Leader • Security Expert • Computer Scientist",
    ),
  ),
)

#let metadata_alt = metadata + (
  layout: metadata.layout + (
    entry: metadata.layout.entry + (
      display_entry_society_first: false,
    )
  )
)

#show: cv.with(
  metadata,
  profile-photo: image("assets/profile/avatar-professional.jpg"),
)

#cv-section("Summary", highlighted: false, letters: 3)

Senior computer scientist, security expert and organizational leader with 30 years of experience across security governance, cloud security architecture, research and engineering. I combine strategic leadership, technical depth and clear communication to help organizations design secure systems, scale teams and deliver measurable outcomes.

#cv-section("Professional Highlights", highlighted: false, letters: 3)

#cv-entry(
  metadata: metadata_alt,
  title: [Management and leadership, IT security, cloud computing],
  society: [],
  date: [],
  location: [],
  description: [
    - Chief Information Security Officer for Governance at #link("https://avaloq.com/")[Avaloq], defining and managing Avaloq's global ISO27001-certified Information Security Management System
- Managed security architecture at the #link("https://www.stellantis.com/en/news/press-releases/2022/january/amazon-stellantis-collaborate-on-software-solutions")[Stellantis _Virtual Engineering Workbench_] project. Worked with Stellantis CISO and business stakeholders to define governance, establish security best practices and drive risk analysis, threat modeling and mitigation.
- Established scalable and durable mechanisms to enable partners to work securely in the #link("https://aws.amazon.com/solutions/case-studies/innovators/volkswagen-group/")[Volkswagen Digital Production Platform (DPP)] program.
- Managed security architecture, risk management, data governance and compliance (ISO27001, ISAE3402/3000, etc.) for #link("https://www.swisscom.ch/en/business/enterprise/offer/cloud-data-center.html")[Swisscom's Cloud platforms].
- Established and led the Swisscom IT Clouds security community of practice.
- Established and led the _Health and State Management_ team at Swisscom to design, implement and operate a framework for scalable monitoring, logging and alerting for Swisscom's Cloud platforms.
- Established and led the first computer security organization at UNAM, which has grown into the university's #link("https://www.seguridad.unam.mx/")[Information Security Coordination (UNAM-CERT)].
- Managed IT security customer relationships at HP Enterprise Services, including overseeing the activities of operational and engineering teams, risk and compliance management, requirements discussion and reporting.
  ]
)

#cv-entry(
  metadata: metadata_alt,
  title: [Research, architecture and design],
  society: [],
  date: [],
  location: [],
  description: [
    - Designed the _Orchard_ monitoring framework for Swisscom's _Application Cloud_ platform, and led the team that implemented it and brought it into production.
- Designed and implemented the _Billy Goat_ malware capture and analysis system at IBM.
  ]
)

#cv-section("Experience", highlighted: false, letters: 3)

#cv-entry(
  title: [CISO Governance],
  society: [#link("https://avaloq.com/")[Avaloq]],
  date: [Jan 2024 - Present],
  location: [Switzerland],
  description: [
    Lead Avaloq's global CISO Governance team and define and monitor the company's Information Security Management System.
- Own security policy and governance direction.
- Provide second-line oversight of first-line security functions.
- Drive compliance monitoring and control effectiveness in a regulated fintech environment.
  ]
)

#cv-entry(
  title: [Global Security Architect / Senior Global Security Architect],
  society: [#link("https://aws.amazon.com/")[Amazon Web Services]],
  date: [Sep 2021 - Dec 2023],
  location: [Switzerland],
  description: [
    Worked with global AWS customers and internal teams to improve security posture, define secure architecture patterns and scale security awareness.
- Led security architecture in the Stellantis Virtual Engineering Workbench program.
- Established security workstreams, metrics and reporting for business and technical stakeholders.
- Helped launch and scale Security Champions and Security Guardians initiatives.
- Supported secure collaboration mechanisms for the Volkswagen Digital Production Platform.
  ]
)

#cv-entry-start(
  society: [#link("https://swisscom.com/")[Swisscom]],
  location: [Switzerland],
)
#v(4pt)

#cv-entry-continued(
  title: [Enterprise Architect and IT Clouds Solution Security Architect],
  date: [Apr 2019 - Sep 2021],
  description: [
    Led security architecture, risk and compliance activities for Swisscom cloud platforms across multiple services.
- Directed compliance and governance activities including ISO27001, ISAE3402/3000 and GDPR requirements.
- Built and led a Security Champions community across IT Clouds teams.
- Coordinated threat modeling, audits, penetration testing and vulnerability management.
  ]
)

#cv-entry-continued(
  title: [Team Lead & Product Owner for Health & State Management],
  date: [Aug 2014 - Apr 2019],
  description: [
    Built and led the Health and State Management team for Swisscom cloud platforms.
- Managed a team of up to 16 people.
- Owned roadmap and prioritization with product managers and stakeholders.
- Defined and delivered platform-wide monitoring, logging and alerting capabilities.
- Led the _Orchard_ project through its implementation, production release and further improvements and development.
  ]
)

#cv-entry(
  title: [Product Manager],
  society: [#link("https://cfengine.com/")[CFEngine AS]],
  date: [Oct 2011 - Jun 2014],
  location: [Norway/U.S.A. (remote)],
  description: [
    - CFEngine Advocate, with a special focus on security.
- Managed the CFEngine language roadmap.
- Created and led the #link("https://docs.cfengine.com/docs/3.10/guide-design-center.html")[CFEngine Design Center] project, which was the foundation for the current #link("https://build.cfengine.com/")[CFEngine Build] service.
- Coordinated the work on CFEngine third-party integration  (e.g. AWS EC2, VMware, Docker and OpenStack).
- Wrote the book #link("https://cf-learn.info/")[_Learning CFEngine 3_], published by O'Reilly Media, which became the de facto introductory text to CFEngine.
  ]
)

#cv-entry(
  title: [Research Staff Member],
  society: [#link("https://research.ibm.com/labs/zurich")[IBM Zurich Research Lab]],
  date: [Oct 2001 - Oct 2009],
  location: [Switzerland],
  description: [
    Member of IBM Zurich's Global Security Analysis Laboratory, working on intrusion detection, malware containment and virtualization security research.
  ]
)

#cv-entry(
  title: [Founder and lead of Computer Security Area],
  society: [#link("https://www.seguridad.unam.mx/")[National Autonomous University of Mexico (UNAM)]],
  date: [Aug 1995 - Aug 1996],
  location: [Mexico],
  description: [
    - Established UNAM's #link("http://www.seguridad.unam.mx/")[_Computer Security Area_], the University's first team dedicated to computer security, which has evolved into the #link("http://www.seguridad.unam.mx/")[_Information Security Coordination (UNAM-CERT)_].
- Managed up to nine people working on different projects related to computer security.
- Provided security services to the whole University, including incident response, security information, auditing and teaching.
  ]
)

#cv-section("Education", highlighted: false, letters: 3)

#cv-entry(
  title: [Ph.D. in Computer Science],
  society: [#link("https://cerias.purdue.edu/")[Purdue University]],
  date: [Aug 1996 - Aug 2001],
  location: [West Lafayette, IN, U.S.A.],
  description: [Thesis: #link("https://zzamboni.org/files/theses/zamboni-phd-thesis.pdf")[Using Internal Sensors for Computer Intrusion Detection]. Advisor: #link("http://spaf.cerias.purdue.edu/")[Eugene H. Spafford]]
)

#cv-entry(
  title: [M.S. in Computer Science],
  society: [#link("https://cerias.purdue.edu/")[Purdue University]],
  date: [Aug 1996 - May 1998],
  location: [West Lafayette, IN, U.S.A.],
  description: [Advisor: #link("http://spaf.cerias.purdue.edu/")[Eugene H. Spafford]]
)

#cv-entry(
  title: [Bachelor's degree in Computer Engineering],
  society: [#link("https://www.unam.mx/")[National Autonomous University of Mexico (UNAM)]],
  date: [Aug 1989 - Jul 1995],
  location: [Mexico City, Mexico],
  description: [Thesis: #link("https://zzamboni.org/files/theses/zamboni-bachelors-thesis.pdf")[UNAM/Cray Project for Security in the Unix Operating System] (in Spanish, original title: _Proyecto UNAM/Cray de Seguridad en el Sistema Operativo Unix_)]
)

#cv-section("Certifications", highlighted: false, letters: 3)

#grid(
  columns: (auto, 1fr),
  column-gutter: 1em,
  align: (center + horizon, left + horizon),
  [#image("assets/badges/6eeb0a98-33cb-4f72-bfc3-f89d65a3286c.png", width: 3em)],
  [
    #link("https://www.credly.com/badges/d74f6e4c-0667-41fb-9243-e11a3793ace4/public_url")[*Certified Information Systems Security Professional (CISSP)*], ISC2 (Apr 2019)
  ]
)

Full list available at #link("https://www.credly.com/users/zzamboni/")[Credly]

#cv-section("Research", highlighted: false, letters: 3)

#cv-entry(
  metadata: metadata_alt,
  title: [#link("https://dominoweb.draco.res.ibm.com/d7c39a9a2e73d870852570060051dfed.html")[Billy Goat: Active worm detection and capture]],
  society: [IBM Research],
  date: [2002 - 2008],
  location: [],
  description: [
    - Pioneered active worm-capture technology that became the foundation for modern honeypots and honeynets
- Designed system to simulate thousands of vulnerable hosts to attract and capture propagating worms
- Implemented automated analysis to extract signatures and update intrusion detection/prevention systems
- Publications: #link("/vita/publications/#pub-riordan06:_build_billy_goat:first2006")[[18]], #link("/vita/publications/#pub-riordan05:bg_techreport")[[25]]
  ]
)

#cv-section("Software", highlighted: false, letters: 3)

#cv-entry(
  metadata: metadata_alt,
  title: [Open-source software projects],
  society: [],
  date: [],
  location: [],
  description: [
    - GitHub: #link("https://github.com/zzamboni")[github.com/zzamboni]
- GitLab: #link("https://gitlab.com/zzamboni")[gitlab.com/zzamboni]
  ]
)

#cv-section("Honors & Awards", highlighted: false, letters: 3)

#cv-honor(
  date: [May 2020],
  title: [IEEE Security & Privacy Test of Time Award (#link("https://www.ieee-security.org/TC/SP2020/awards.html")[IEEE S&P page], #link("https://www.cerias.purdue.edu/site/blog/post/a_test_of_time_coast_and_an_award-winning_paper/")[CERIAS blog post])],
  issuer: [IEEE],
)
#v(6pt)

#cv-honor(
  date: [2010],
  title: [#link("https://cfengine.com/engage/cfengine-champions/")[CFEngine Champion]],
  issuer: [CFEngine AS],
)
#v(6pt)

#cv-honor(
  date: [May 1996],
  title: [Fulbright Scholarship (for pursuing Ph.D. studies at Purdue University)],
  issuer: [Fulbright Program and CONACYT],
)
#v(6pt)

#cv-section("Selected publications", highlighted: false, letters: 3)

#refsection(format-citation: publications-style.format-citation)[
  #print-bibliography(
    format-reference: format-reference(reference-label: publications-style.reference-label),
    title: "Books",
    label-generator: publications-style.label-generator,
    sorting: "ydnt",
    show-all: true,
    resume-after: auto,
    filter: reference => publications-include(reference) and has-keyword(reference.fields.at("keywords", default: none), "book")
  )
  #print-bibliography(
    format-reference: format-reference(reference-label: publications-style.reference-label),
    title: "Theses",
    label-generator: publications-style.label-generator,
    sorting: "ydnt",
    show-all: true,
    resume-after: auto,
    filter: reference => publications-include(reference) and has-keyword(reference.fields.at("keywords", default: none), "thesis")
  )
  #print-bibliography(
    format-reference: format-reference(reference-label: publications-style.reference-label),
    title: "Refereed Papers",
    label-generator: publications-style.label-generator,
    sorting: "ydnt",
    show-all: true,
    resume-after: auto,
    filter: reference => publications-include(reference) and has-keyword(reference.fields.at("keywords", default: none), "refereed")
  )
  #print-bibliography(
    format-reference: format-reference(reference-label: publications-style.reference-label),
    title: "Presentations at Conferences and Workshops",
    label-generator: publications-style.label-generator,
    sorting: "ydnt",
    show-all: true,
    resume-after: auto,
    filter: reference => publications-include(reference) and has-keyword(reference.fields.at("keywords", default: none), "presentations")
  )
  #print-bibliography(
    format-reference: format-reference(reference-label: publications-style.reference-label),
    title: "Invited Talks and Articles",
    label-generator: publications-style.label-generator,
    sorting: "ydnt",
    show-all: true,
    resume-after: auto,
    filter: reference => publications-include(reference) and has-keyword(reference.fields.at("keywords", default: none), "invited")
  )
]

#cv-section("Skills", highlighted: false, letters: 3)

#cv-skill(type: [Leadership], info: [32 years of multidisciplinary team and project leadership experience #sym.dot.c IT Enterprise Architecture #sym.dot.c Scaled Agile Framework (SAFe)])
#v(6pt)

#cv-skill(type: [Information and Cyber Security], info: [Enterprise security governance #sym.dot.c Enterprise security architecture #sym.dot.c Virtualization and cloud computing security #sym.dot.c Risk management and compliance #sym.dot.c Intrusion detection and prevention #sym.dot.c Software security and secure software development #sym.dot.c ISO27001])
#v(6pt)

#cv-skill(type: [Technology], info: [Broad and deep IT expertise #sym.dot.c Cloud computing #sym.dot.c Computer security #sym.dot.c Operating systems #sym.dot.c Networking #sym.dot.c Configuration management #sym.dot.c Software & services development #sym.dot.c Programming languages])
#v(6pt)

#cv-skill(type: [Research], info: [Ph.D. in Computer Science #sym.dot.c 9 years of experience at IBM Research])
#v(6pt)

#cv-skill(type: [Communication], info: [Excellent written and spoken communication skills #sym.dot.c Extensive public speaking experience #sym.dot.c Professional writing and teaching experience])
#v(6pt)

#cv-section("Languages", highlighted: false, letters: 3)

#cv-skill(type: [Spanish], info: [Native])

#cv-skill(type: [English], info: [Full proficiency])

#cv-skill(type: [German], info: [Intermediate proficiency (B2 level)])

#cv-section("Other Professional Activities", highlighted: false, letters: 3)

#cv-entry(
  title: [Member],
  society: [#link("http://www.acm.org/")[The Association for Computing Machinery (ACM)]],
  date: [1998 - Present],
  location: [],
  description: []
)

#cv-entry(
  title: [Secretary and President],
  society: [#link("https://www.cs.purdue.edu/future-students/organizations.html")[Purdue University Chapter of Upsilon Pi Epsilon]],
  date: [1998 - 2000],
  location: [],
  description: []
)

#cv-section("References", highlighted: false, letters: 3)

- Available by request

