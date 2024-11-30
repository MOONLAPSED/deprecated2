import math
import random
import cmath

class QuantumInfoDynamics:
    def __init__(self, dimensions=3):
        self.dimensions = dimensions
        self.state = [random.random() for _ in range(dimensions)]
        self._normalize()

    @property
    def state(self):
        return self._state.copy()

    @state.setter
    def state(self, value):
        self._state = value
        self._normalize()

    def _normalize(self):
        norm = math.sqrt(sum(x ** 2 for x in self._state))
        self._state = [x / norm for x in self._state]

    def rotate(self, axis, angle):
        # Use basic rotation formulae, we'll stick to 2D or simple 3D rotations
        if len(axis) != 3 or len(self._state) != 3:
            raise ValueError("Currently, only 3D rotations are supported.")

        x, y, z = self._state
        u, v, w = axis
        ux, uy, uz = u * x, u * y, u * z
        vx, vy, vz = v * x, v * y, v * z
        wx, wy, wz = w * x, w * y, w * z

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        self._state = [
            u * (ux + vy + wz) + (x * (v * v + w * w) - u * (vy + wz)) * cos_a + (-wy + vz) * sin_a,
            v * (ux + vy + wz) + (y * (u * u + w * w) - v * (ux + wz)) * cos_a + (wx - uz) * sin_a,
            w * (ux + vy + wz) + (z * (u * u + v * v) - w * (ux + vy)) * cos_a + (-vx + uy) * sin_a
        ]
        self._normalize()

    def interact(self, other):
        if len(self._state) != 3 or len(other.state) != 3:
            raise ValueError("Currently, only 3D interactions (cross product) are supported.")
        x1, y1, z1 = self._state
        x2, y2, z2 = other.state
        interaction = [
            y1 * z2 - z1 * y2,
            z1 * x2 - x1 * z2,
            x1 * y2 - y1 * x2
        ]
        self.state = [a + b for a, b in zip(self._state, interaction)]
        other.state = [a + b for a, b in zip(other.state, interaction)]
        self._normalize()
        other._normalize()

    def measure(self):
        return sum(x ** 2 for x in self._state)


class TripartiteState:
    def __init__(self, *args):
        if len(args) != 4:
            raise ValueError(
                "TripartiteState must be initialized with exactly 4 arguments"
            )
        self.q = list(map(complex, args))

    @property
    def q(self):
        return self._q.copy()

    @q.setter
    def q(self, value):
        self._q = value

    def __mul__(self, other):
        a1, b1, c1, d1 = self.q
        a2, b2, c2, d2 = other.q
        return TripartiteState(
            a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
            a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
            a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
        )

    def conjugate(self):
        return TripartiteState(*[x.conjugate() for x in self.q])

    @property
    def norm(self):
        return math.sqrt(sum(abs(x) ** 2 for x in self.q))


def rotate(state, axis, angle):
    half_angle = angle / 2
    sin_half = cmath.sin(half_angle)
    cos_half = cmath.cos(half_angle)

    if axis[0] == 1:
        euler_angles = (0, cmath.phase(sin_half), 0)
    elif axis[1] == 1:
        euler_angles = (0, cmath.phase(sin_half), 0)
    elif axis[2] == 1:
        euler_angles = (cmath.phase(cos_half), 0, 0)

    state_q_list = state.q
    rotated_state_q = []
    for q in state_q_list:
        q_real = q.real
        q_imag = q.imag
        q_x = q_real
        q_y = q_imag
        q_z = 0  
        rotated_q = cmath.rect(math.hypot(q_x, q_y), cmath.phase(q) + euler_angles[0])
        rotated_state_q.append(complex(rotated_q.real, rotated_q.imag))

    return TripartiteState(*rotated_state_q)

if __name__ == "__main__":
    for i in range(0, 360, 10):
        state = TripartiteState(1, 0, 0, 0)
        rotated_state = rotate(state, (0, 0, 1), i)
        print(f'Angle : {i} degrees')
        print(f'Rotated State : {rotated_state.q}')