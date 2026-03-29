const audioCache = {}

export function playAudio(name) {
  try {
    if (!audioCache[name]) {
      audioCache[name] = new Audio(`/src/assets/audio/${name}.mp3`)
    }
    audioCache[name].currentTime = 0
    audioCache[name].play().catch(() => {})
  } catch {}
}
