// Publications list generated from BibTeX
// Using brilliant-cv template for document layout

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
  awesome-colors: none,
  awesomeColors: _awesome-colors,
) = context {
  let metadata = if metadata != none { metadata } else { cv-metadata.get() }
  let awesome-colors = if awesome-colors != none {
    awesome-colors
  } else {
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

#add-bib-resource(read("zamboni-vita-pubs.bib"))

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
      location: "Zurich, CH",
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
      fonts: (
      regular_fonts: ("Source Sans 3",),
      header_font: "Roboto"
    ),
      header: (
      header_align: "left",
      display_profile_photo: true,
      profile_photo_radius: "50%",
      info_font_size: "10pt"
    ),
      entry: (
      display_entry_society_first: true,
      display_logo: true
    ),
      footer: (
      display_page_counter: true,
      display_footer: true
    )
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

#let metadata_pub = metadata + (
  personal: metadata.personal + (
    info: (),
  ),
  layout: metadata.layout + (
    header: metadata.layout.header + (
      display_profile_photo: false,
    ),
  ),
  lang: metadata.lang + (
    en: metadata.lang.en + (
      cv_footer: [ Selected publications - #datetime.today().display() ],
      header_quote: "",
    ),
  ),
)

#show: cv.with(
  metadata_pub,
)

#cv-section("Selected publications", highlighted: false)

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
    title: "Editorial Activities",
    label-generator: publications-style.label-generator,
    sorting: "ydnt",
    show-all: true,
    resume-after: auto,
    filter: reference => publications-include(reference) and has-keyword(reference.fields.at("keywords", default: none), "editorial")
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
]

