export const situations = [
  {
    id: 'labour',
    title: 'Labour Rights',
    titleHi: 'श्रमिक अधिकार',
    description: 'Wages, working conditions & employment disputes',
    color: 'green',
    situationType: 'labour',
    rights: [
      'Minimum wages are legally guaranteed under the Code on Wages, 2019 — no employer can pay less.',
      'Working hours cannot exceed 8 hours/day or 48 hours/week. Overtime must be paid at 2× the normal rate.',
      'Every worker is entitled to weekly rest, paid national holidays, and earned leave.',
      'Termination without notice or valid reason entitles you to compensation under the Industrial Disputes Act.',
      'Bonded labour is a criminal offence under the Bonded Labour System (Abolition) Act, 1976.',
    ],
  },
  {
    id: 'domestic_violence',
    title: 'Domestic Violence',
    titleHi: 'घरेलू हिंसा',
    description: 'Protection, shelter & legal remedies for abuse',
    color: 'red',
    situationType: 'family_dv',
    rights: [
      'The Protection of Women from Domestic Violence Act, 2005 covers physical, emotional, verbal, sexual, and economic abuse.',
      'You have the right to reside in the shared household — no one can evict you illegally.',
      'You can get a Protection Order from a Magistrate preventing the abuser from contacting or harming you.',
      'Free legal aid is available through DLSA. You do not need money to file a case.',
      'Section 498A IPC allows criminal prosecution for cruelty by husband or his relatives.',
    ],
  },
  {
    id: 'land_property',
    title: 'Land & Property',
    titleHi: 'भूमि एवं संपत्ति',
    description: 'Ownership, disputes, tenant & inheritance rights',
    color: 'amber',
    situationType: 'civil',
    rights: [
      'All property records must be registered under the Registration Act, 1908 — unregistered sales are not valid for immovable property over ₹100.',
      'Hindu women have equal coparcenary rights in ancestral property since the 2005 amendment to the Hindu Succession Act.',
      'Tenants have protection against arbitrary eviction under state-specific Rent Control Acts.',
      'Land acquisition requires fair compensation, rehabilitation, and consent under the RFCTLARR Act, 2013.',
      'Revenue court records (khata/khasra/jamabandi) are your primary proof of land ownership.',
    ],
  },
  {
    id: 'sc_st',
    title: 'SC/ST Rights',
    titleHi: 'अनुसूचित जाति/जनजाति अधिकार',
    description: 'Anti-discrimination, reservations & atrocity prevention',
    color: 'purple',
    situationType: 'scst',
    rights: [
      'The SC/ST Prevention of Atrocities Act, 1989 criminalises caste-based violence, humiliation, and discrimination.',
      'FIR registration is mandatory and cannot be refused for atrocity complaints — officers who refuse face action.',
      'Victims are entitled to immediate relief of ₹8.25 lakh (varies by offence) under the 2016 Rules.',
      'Constitutional reservations in education and public employment are a fundamental right under Articles 15(4) and 16(4).',
      'Exclusive Special Courts ensure speedy trial for cases under the Atrocities Act.',
    ],
  },
];

export const colorMap = {
  green: {
    bg: 'bg-emerald-50 dark:bg-emerald-950/40',
    border: 'border-emerald-200 dark:border-emerald-800',
    text: 'text-emerald-800 dark:text-emerald-300',
    accent: 'bg-emerald-600',
    pill: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300',
    hover: 'hover:border-emerald-400 hover:shadow-emerald-100 dark:hover:border-emerald-600 dark:hover:shadow-none',
  },
  red: {
    bg: 'bg-red-50 dark:bg-red-950/40',
    border: 'border-red-200 dark:border-red-800',
    text: 'text-red-800 dark:text-red-300',
    accent: 'bg-red-600',
    pill: 'bg-red-100 text-red-800 dark:bg-red-900/60 dark:text-red-300',
    hover: 'hover:border-red-400 hover:shadow-red-100 dark:hover:border-red-600 dark:hover:shadow-none',
  },
  amber: {
    bg: 'bg-amber-50 dark:bg-amber-950/40',
    border: 'border-amber-200 dark:border-amber-800',
    text: 'text-amber-800 dark:text-amber-300',
    accent: 'bg-amber-600',
    pill: 'bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-300',
    hover: 'hover:border-amber-400 hover:shadow-amber-100 dark:hover:border-amber-600 dark:hover:shadow-none',
  },
  purple: {
    bg: 'bg-purple-50 dark:bg-purple-950/40',
    border: 'border-purple-200 dark:border-purple-800',
    text: 'text-purple-800 dark:text-purple-300',
    accent: 'bg-purple-600',
    pill: 'bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-300',
    hover: 'hover:border-purple-400 hover:shadow-purple-100 dark:hover:border-purple-600 dark:hover:shadow-none',
  },
  blue: {
    bg: 'bg-blue-50 dark:bg-blue-950/40',
    border: 'border-blue-200 dark:border-blue-800',
    text: 'text-blue-800 dark:text-blue-300',
    accent: 'bg-blue-600',
    pill: 'bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300',
    hover: 'hover:border-blue-400 hover:shadow-blue-100 dark:hover:border-blue-600 dark:hover:shadow-none',
  },
  gray: {
    bg: 'bg-gray-50 dark:bg-gray-800/60',
    border: 'border-gray-200 dark:border-gray-700',
    text: 'text-gray-700 dark:text-gray-300',
    accent: 'bg-gray-500',
    pill: 'bg-gray-100 text-gray-700 dark:bg-gray-700/60 dark:text-gray-300',
    hover: 'hover:border-gray-400 hover:shadow-gray-100 dark:hover:border-gray-500 dark:hover:shadow-none',
  },
};

export const domainColorKey = {
  labour: 'green',
  family_dv: 'red',
  civil: 'amber',
  criminal: 'red',
  rti: 'blue',
  scst: 'purple',
  unclear: 'gray',
};

export const domainLabels = {
  labour: 'Labour',
  family_dv: 'Domestic Violence',
  civil: 'Civil / Property',
  criminal: 'Criminal',
  rti: 'RTI',
  scst: 'SC/ST Rights',
  unclear: 'Unclassified',
};

export const letterTypeLabels = {
  labour_complaint: 'Labour Complaint Letter',
  rti_application: 'RTI Application',
  fir_draft: 'FIR Draft',
  dv_protection_order: 'DV Protection Order',
};
