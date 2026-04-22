export type Article = {
  slug: string;
  kicker: string;
  topic: string;
  headline: string;
  dek: string;
  byline: string;
  location: string;
  date: string;
  readTime: string;
  lead: string;
  body: { type: "p" | "h2" | "pull"; text: string }[];
};

export const articles: Article[] = [
  {
    slug: "fishing-fleets-that-dont-come-home",
    kicker: "Field report",
    topic: "Labor trafficking",
    headline: "The fishing fleets that don't come home",
    dek: "How forced labor survives in the blank spaces between jurisdictions — and who is quietly mapping them.",
    byline: "Ava Okonkwo",
    location: "Songkhla, Thailand",
    date: "April 2026",
    readTime: "14 min",
    lead: "The boats leave from small ports in the Gulf of Thailand and the Andaman Sea, and some of them do not come back for two years. When they do, the men aboard are sometimes not the men who left.",
    body: [
      { type: "p", text: "There is a phrase that recurs in the testimonies: \"the ocean has no country.\" It is used by traffickers as a boast and by survivors as a kind of mourning. Out past the territorial waters of any coastal state, a boat becomes its own jurisdiction, answerable only to its captain. The International Labour Organization estimates that several hundred thousand men are held in conditions of forced labor on commercial fishing vessels worldwide at any given moment. The estimate is rough because the people being counted are not permitted to be counted." },
      { type: "h2", text: "The geometry of invisibility" },
      { type: "p", text: "What makes the trade so durable is not the cruelty of any single operator. It is the geometry. A man recruited in a Cambodian village can be trafficked through three middlemen, transshipped at sea between vessels that never return to port, and worked for two years without ever touching land in a country that has recorded his existence. The paperwork, when there is any, belongs to ships flagged in states that have neither the capacity nor the incentive to verify crew lists." },
      { type: "pull", text: "\"The ocean has no country.\" Traffickers say it as a boast. Survivors say it as a kind of mourning." },
      { type: "p", text: "But geometry can be mapped. Over the last four years a small coalition of data journalists, port-state inspectors, and former sailors has been assembling what amounts to an atlas of the invisible — a record of vessel movements, transshipment patterns, and port calls that, read together, begin to show the shape of the trade." },
      { type: "h2", text: "Reading a ship's silence" },
      { type: "p", text: "The work depends, strangely, on silence. Every commercial vessel over a certain size is required to broadcast its position via AIS, a maritime transponder system. When a boat turns its AIS off for days at a time in waters where other vessels don't, that absence is itself a signal. The atlas — maintained by a nonprofit called Sea Watch Labs — treats AIS gaps as investigative leads rather than noise." },
      { type: "p", text: "None of this rescues the men on the boats. What it does, its architects argue, is make the trade legible enough that the institutions nominally responsible for it cannot plausibly claim not to see." },
    ],
  },
  {
    slug: "country-without-a-coastline",
    kicker: "Analysis",
    topic: "Climate displacement",
    headline: "A country without a coastline",
    dek: "When a nation is promised to disappear, its people become a category no passport office has a name for.",
    byline: "Reyes Martín",
    location: "Funafuti, Tuvalu",
    date: "March 2026",
    readTime: "9 min",
    lead: "In a small office on a narrow strip of coral, a government is writing the legal instruments of its own afterlife.",
    body: [
      { type: "p", text: "Tuvalu has nine islands, none of which rise more than five meters above sea level, and a population that could fit inside a mid-sized football stadium. It is also, as of last year, the first country to be recognized by treaty as a continuing state even in the event that all of its territory becomes uninhabitable. The recognition is Australia's. It is unprecedented. And it raises a question that international law is not yet built to answer." },
      { type: "pull", text: "What does it mean to be a citizen of a country that no longer has a coastline?" },
      { type: "p", text: "The answer, for now, is that no one quite knows. A Tuvaluan passport, under the new arrangement, remains valid even after the islands are gone. The government, in exile, retains its seat at the United Nations. The flag continues to be raised. What is missing is everything a state is supposed to stand on — the land, the coastline, the waters claimed by extension." },
      { type: "h2", text: "A category with one member" },
      { type: "p", text: "The Tuvaluan case is singular, but it will not be for long. Kiribati, the Marshall Islands, parts of the Maldives, and a number of Pacific atolls are in various stages of the same conversation, often with the same treaty lawyers. The scholars who work on this call it \"deterritorialized statehood,\" and the phrase carries the dryness of something that has not yet been tested by a real case." },
    ],
  },
  {
    slug: "offline-by-design",
    kicker: "Investigation",
    topic: "Digital exclusion",
    headline: "Offline by design",
    dek: "Millions are locked out of benefits, banking, and identity itself — not by accident, but by the shape of the system.",
    byline: "Priya Banerjee",
    location: "Hyderabad, India",
    date: "March 2026",
    readTime: "12 min",
    lead: "The woman in the photograph is holding a piece of paper that says, in English and in Telugu, that she does not exist.",
    body: [
      { type: "p", text: "Her name is Lakshmi. She is forty-three, a widow, a daily-wage worker, and, as of the last biometric enrollment drive in her district, officially absent from the national identity database. Her fingerprints, worn smooth by two decades of agricultural labor, no longer register cleanly on the scanners that now mediate her access to food rations, to her widow's pension, to the bank account into which that pension is meant to be deposited." },
      { type: "h2", text: "The architecture of exclusion" },
      { type: "p", text: "A system like Aadhaar, India's national identity program, enrolls more than a billion people. It is, by most measures, an administrative triumph. It also produces, as a byproduct of its own architecture, a category of people who become less visible to the state in exact proportion to the system's success." },
      { type: "pull", text: "The system did not fail Lakshmi. The system is working as designed. Lakshmi is one of the things it is designed to produce." },
      { type: "p", text: "The people who fall out of such systems are not random. They are disproportionately older, rural, female, and poor — which is to say, the people the system was ostensibly built to serve." },
    ],
  },
  {
    slug: "the-hotline-nobody-answers",
    kicker: "Dispatch",
    topic: "Anti-trafficking",
    headline: "The hotline that nobody answers",
    dek: "Why the infrastructure built to receive cries for help is often the first thing traffickers learn to silence.",
    byline: "Jonah Lister",
    location: "Lagos, Nigeria",
    date: "February 2026",
    readTime: "11 min",
    lead: "In a windowless room in a Lagos suburb, a phone rings and rings and is not answered, because the person employed to answer it was laid off in the last funding cycle.",
    body: [
      { type: "p", text: "The hotline was set up in 2019 with money from a European donor and staffed by four trained counselors. By 2023, two of them had been let go. By last year, the line was being forwarded to a volunteer's personal mobile. The calls, meanwhile, have not decreased." },
      { type: "pull", text: "A hotline is only as useful as the infrastructure behind it. Traffickers know this faster than funders do." },
      { type: "h2", text: "What traffickers learn" },
      { type: "p", text: "Traffickers, it turns out, study these systems with the attention of auditors. They know which hotlines are staffed overnight and which are not. They know which ones route to national police and which to NGO casework. They adjust their operations accordingly. The hotline is not merely a service. It is a piece of intelligence, and its weaknesses are, from the traffickers' perspective, operational advantages." },
    ],
  },
  {
    slug: "care-without-a-clinic",
    kicker: "Essay",
    topic: "Mental health",
    headline: "What care looks like without a clinic",
    dek: "In the places where psychiatry never arrived, communities are building something it couldn't have imagined.",
    byline: "Tess Nambale",
    location: "Gulu, Uganda",
    date: "February 2026",
    readTime: "8 min",
    lead: "The treatment takes place under a mango tree. There is no intake form. There is, however, a great deal of listening.",
    body: [
      { type: "p", text: "Northern Uganda has, by any accounting, one of the worst mental-health burdens in the world — two decades of civil war followed by twenty years of its aftermath. It also has, at last count, fewer than a dozen licensed psychiatrists for a population of several million. The arithmetic does not work. It was never going to work. And so something else had to be built." },
      { type: "h2", text: "The lay counselor model" },
      { type: "p", text: "What was built, over the last fifteen years, is a network of lay counselors — community members trained in a compressed version of evidence-based talk therapy, supervised by a small number of clinicians, and deployed in the villages where they already live. The model has been studied, replicated, and in several rigorous trials shown to produce outcomes comparable to formal psychiatric care for common conditions." },
      { type: "pull", text: "The absence of a clinic turned out to be less of an obstacle than the assumption that a clinic was the only shape care could take." },
    ],
  },
];

export function getArticle(slug: string): Article | undefined {
  return articles.find((a) => a.slug === slug);
}
