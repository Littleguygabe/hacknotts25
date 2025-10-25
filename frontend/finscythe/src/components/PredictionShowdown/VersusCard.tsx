import vsImage from '@/assets/comic-style-duel-conflict-versus-vs-banner-design.png';

export function VersusCard() {
  return (
  <div className="flex justify-center items-center w-108 h-108 bg-transparent">
    <img src={vsImage} alt="Versus" className="w-full h-full object-cover" />
  </div>
  );
}