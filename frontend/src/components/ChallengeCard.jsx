export default function ChallengeCard({ challenge }) {
  return (
    <article className={`challenge-card ${challenge.solved ? 'solved-card' : ''}`}>
      <div className="challenge-meta">
        <span>{challenge.category}</span>
        <strong>{challenge.points} pts</strong>
      </div>
      <div className="badge-row">
        <span className="difficulty-badge">{challenge.difficulty}</span>
        {challenge.solved && <span className="solved-badge">Solved</span>}
      </div>
      <h3>{challenge.title}</h3>
      <p>{challenge.description}</p>
      {challenge.hint && <p className="hint"><strong>Hint:</strong> {challenge.hint}</p>}
      <code>{challenge.slug}</code>
    </article>
  )
}