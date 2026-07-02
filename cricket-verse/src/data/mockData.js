export const mockMatches = [
  {
    id: 1,
    status: 'live',
    type: 'T20 World Cup Final',
    team1: { name: 'India', code: 'IND', score: '185/4', overs: '19.2', logo: '🇮🇳' },
    team2: { name: 'Australia', code: 'AUS', score: '176/8', overs: '20.0', logo: '🇦🇺' },
    summary: 'India need 10 runs in 4 balls',
  },
  {
    id: 2,
    status: 'upcoming',
    type: 'Test Series - Match 1',
    team1: { name: 'England', code: 'ENG', logo: '🏴󠁧󠁢󠁥󠁮󠁧󠁿' },
    team2: { name: 'South Africa', code: 'RSA', logo: '🇿🇦' },
    time: 'Tomorrow, 10:00 AM',
  },
  {
    id: 3,
    status: 'completed',
    type: 'ODI Series',
    team1: { name: 'New Zealand', code: 'NZ', score: '280/8', overs: '50.0', logo: '🇳🇿' },
    team2: { name: 'Pakistan', code: 'PAK', score: '275/10', overs: '49.1', logo: '🇵🇰' },
    summary: 'New Zealand won by 5 runs',
  }
];

export const mockTeams = [
  { id: 1, name: 'India', code: 'IND', ranking: 1, captain: 'Rohit Sharma', flag: '🇮🇳' },
  { id: 2, name: 'Australia', code: 'AUS', ranking: 2, captain: 'Pat Cummins', flag: '🇦🇺' },
  { id: 3, name: 'England', code: 'ENG', ranking: 3, captain: 'Jos Buttler', flag: '🏴󠁧󠁢󠁥󠁮󠁧󠁿' },
  { id: 4, name: 'New Zealand', code: 'NZ', ranking: 4, captain: 'Kane Williamson', flag: '🇳🇿' },
  { id: 5, name: 'South Africa', code: 'RSA', ranking: 5, captain: 'Temba Bavuma', flag: '🇿🇦' },
  { id: 6, name: 'Pakistan', code: 'PAK', ranking: 6, captain: 'Babar Azam', flag: '🇵🇰' },
];

export const mockPlayers = [
  { id: 1, name: 'Virat Kohli', team: 'India', role: 'Batsman', average: 50.3, strikeRate: 138.1, matches: 115, image: 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60' },
  { id: 2, name: 'Pat Cummins', team: 'Australia', role: 'Bowler', wickets: 120, economy: 7.2, matches: 85, image: 'https://images.unsplash.com/photo-1531415074968-036ba1b575da?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60' },
  { id: 3, name: 'Ben Stokes', team: 'England', role: 'All-rounder', average: 38.5, wickets: 85, matches: 90, image: 'https://images.unsplash.com/photo-1593341646782-e0b495cff86d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60' },
  { id: 4, name: 'Jasprit Bumrah', team: 'India', role: 'Bowler', wickets: 145, economy: 6.5, matches: 70, image: 'https://images.unsplash.com/photo-1593341646782-e0b495cff86d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60' },
];

export const mockTrivia = [
  "Did you know? The longest cricket match in history was between England and South Africa in 1939. It lasted for 14 days and finally ended in a draw because the English team had to catch a boat home!",
  "Sachin Tendulkar is the only player to score 100 international centuries.",
  "The first official cricket test match was played in 1877 between Australia and England.",
  "Sir Don Bradman has an incredible test batting average of 99.94.",
];
