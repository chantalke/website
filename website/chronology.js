// Only confirmed full dates; a year-only record is not assigned a fictitious day.
const CONFIRMED_DATES={S001:'2024-11-05',M003:'2024-11-05',S007:'2015-04-15',S009:'2016-02-16',S010:'2016-04-19',M004:'2016-02-11',M005:'2013-02-28'};
function compareTimeline(a,b){
  const yearA=Number(String(a.year||'').match(/\b(?:19|20)\d{2}\b/)?.[0]||0);
  const yearB=Number(String(b.year||'').match(/\b(?:19|20)\d{2}\b/)?.[0]||0);
  if(yearA!==yearB)return yearB-yearA;
  const dateA=CONFIRMED_DATES[a.id],dateB=CONFIRMED_DATES[b.id];
  if(dateA&&dateB)return dateB.localeCompare(dateA);
  // Within a year, place records with a confirmed day before year-only records.
  return Number(Boolean(dateB))-Number(Boolean(dateA));
}
function timelineDate(id,year){const date=CONFIRMED_DATES[id];if(!date)return year||(document.documentElement.lang==='en'?'Undated':'Ongedateerd');return new Intl.DateTimeFormat(document.documentElement.lang==='en'?'en-GB':'nl-NL',{day:'numeric',month:'short',year:'numeric',timeZone:'UTC'}).format(new Date(date+'T12:00:00Z'));}
