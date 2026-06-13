const coordinators = [
  {
    name: 'Sujith Kumar',
    role: 'Senior Coordinator',
    linkedin: 'https://www.linkedin.com/in/sujith-eag/'
    
  },
  {
    name: 'V Varun Murthy',
    role: 'Junior Coordinator',
    linkedin: 'https://www.linkedin.com/in/varun-murthy-131200383/'
  },
  {
    name: 'Sinchana Shetty',
    role: 'Junior Coordinator',
    linkedin: 'https://www.linkedin.com/in/sinchana-shetty2004/'
  }
]

export default function Footer() {
  return (
    <footer className="footer" data-footer-static="CTF{static_at_the_footer}">
      <p>Shadow Protocol · CTF Event Operations</p>
      <p>Investigate only the provided challenge scope and authorized lab routes.</p>

      <div className="footer-socials">
        <span>Event Coordinators:</span>
        {coordinators.map((person) => (
          <a
            key={person.linkedin}
            href={person.linkedin}
            target="_blank"
            rel="noreferrer"
            className="footer-social-link"
            title={person.role}
          >
            {person.name}
          </a>
        ))}
      </div>
    </footer>
  )
}
