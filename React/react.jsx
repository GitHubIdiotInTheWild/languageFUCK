import { useState } from 'react';

export default function App() {
  const [xp, setXp] = useState(0);
  const [quests, setQuests] = useState([
    { id: 1, text: "Defeat the Dragon" },
    { id: 2, text: "Clean your room dungeon" }
  ]);
  const [newQuestText, setNewQuestText] = useState("");

  const completeQuest = (id) => {
    setQuests(quests.filter(quest => quest.id !== id));
    setXp(xp + 50);
  };

  const addQuest = (e) => {
    e.preventDefault();
    if (!newQuestText.trim()) return;
    setQuests([...quests, { id: Date.now(), text: newQuestText }]);
    setNewQuestText("");
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', background: '#222', color: '#fff', minHeight: '100vh' }}>
      <h1>⚔️ Hero's Quest Log</h1>
      <h2>Level: {Math.floor(xp / 100) + 1} | XP: {xp}</h2>
      <hr />
      <form onSubmit={addQuest} style={{ margin: '20px 0' }}>
        <input 
          type="text" 
          placeholder="Enter a new quest..." 
          value={newQuestText}
          onChange={(e) => setNewQuestText(e.target.value)}
          style={{ padding: '8px', width: '250px', marginRight: '10px' }}
        />
        <button type="submit" style={{ padding: '8px 12px' }}>Add Quest</button>
      </form>
      <h3>Active Quests:</h3>
      {quests.length === 0 ? <p>All quests cleared! 🎉</p> : null}
      <ul>
        {quests.map(quest => (
          <li key={quest.id} style={{ margin: '10px 0' }}>
            {quest.text} {' '}
            <button onClick={() => completeQuest(quest.id)}>Complete (+50 XP)</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
