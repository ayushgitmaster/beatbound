import { useRef, useMemo, Suspense } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Environment } from '@react-three/drei'
import * as THREE from 'three'

/** Build an extruded 3-D heart geometry centred at the origin. */
function buildHeartGeometry(): THREE.ExtrudeGeometry {
  const shape = new THREE.Shape()

  // Heart path: lobes at top (y+), pointed tip at bottom (y-)
  shape.moveTo(0, 0.35)
  shape.bezierCurveTo(-0.04, 0.64, -0.52, 0.92, -0.84, 0.73)
  shape.bezierCurveTo(-1.18, 0.52, -1.18, 0.09, -1.18, 0.03)
  shape.bezierCurveTo(-1.18, -0.37, -0.62, -0.77, 0.00, -1.06)
  shape.bezierCurveTo( 0.62, -0.77,  1.18, -0.37,  1.18,  0.03)
  shape.bezierCurveTo( 1.18,  0.09,  1.18,  0.52,  0.84,  0.73)
  shape.bezierCurveTo( 0.52,  0.92,  0.04,  0.64,  0.00,  0.35)

  const geo = new THREE.ExtrudeGeometry(shape, {
    depth: 0.38,
    bevelEnabled: true,
    bevelThickness: 0.26,
    bevelSize: 0.22,
    bevelSegments: 14,
    curveSegments: 64,
  })

  // Centre geometry so the heart rotates around its own middle
  geo.center()
  return geo
}

function HeartMesh() {
  const ref = useRef<THREE.Mesh>(null!)
  const geometry = useMemo(buildHeartGeometry, [])

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime()

    // Gentle orbital tilt — gives the "3-D rotating logo" feel
    ref.current.rotation.y = Math.sin(t * 0.38) * 0.40
    ref.current.rotation.x = Math.sin(t * 0.22) * 0.06 - 0.06

    // Realistic double-pump heartbeat at ~72 bpm (cycle = 0.833 s)
    const c = t % 0.833
    let s = 1.0
    if      (c < 0.07) s = 1.00 + (c / 0.07) * 0.13               // lub — squeeze up
    else if (c < 0.14) s = 1.13 - ((c - 0.07) / 0.07) * 0.08      // lub — release
    else if (c < 0.21) s = 1.05 + ((c - 0.14) / 0.07) * 0.07      // dub — squeeze up
    else if (c < 0.31) s = 1.12 - ((c - 0.21) / 0.10) * 0.12      // dub — release
    // rest of cycle: s stays at 1.0

    ref.current.scale.setScalar(s)
  })

  return (
    <mesh ref={ref} geometry={geometry} castShadow>
      <meshPhysicalMaterial
        color="#c01030"
        roughness={0.28}
        metalness={0.06}
        clearcoat={0.95}
        clearcoatRoughness={0.12}
        emissive="#8a001e"
        emissiveIntensity={0.42}
        envMapIntensity={1.15}
      />
    </mesh>
  )
}

interface HeartCanvasProps {
  size?: number
}

export default function HeartCanvas({ size = 300 }: HeartCanvasProps) {
  return (
    <div style={{ width: size, height: size, flexShrink: 0 }}>
      <Canvas
        shadows
        camera={{ position: [0, 0, 6.5], fov: 44 }}
        gl={{ alpha: true, antialias: true, powerPreference: 'high-performance' }}
        style={{ display: 'block', width: '100%', height: '100%', background: 'transparent' }}
      >
        {/* Key light */}
        <pointLight position={[2.5, 3.5, 3.5]} intensity={3.2} color="#ffffff" castShadow />
        {/* Rim / fill in red to reinforce the heart colour */}
        <pointLight position={[-3, 1, 2]}       intensity={1.0} color="#ff3050" />
        {/* Soft under-bounce */}
        <pointLight position={[0, -2, 4]}        intensity={0.55} color="#ffb0b0" />
        <ambientLight intensity={0.45} />

        <Suspense fallback={null}>
          <Environment preset="sunset" />
          <HeartMesh />
        </Suspense>
      </Canvas>
    </div>
  )
}
