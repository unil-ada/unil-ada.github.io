# Lecture 13 (reinforcement learning) — demo notebooks

Private maintenance note. Not published to the students.

## Source

Four demo notebooks from Simon Scheidegger's 2025 RL lecture (week 13, 7 December),
carried over unchanged from earlier years:

| notebook | upstream origin |
| --- | --- |
| `demo/rl-basics.ipynb` | REINFORCE on CartPole, after Chinmay Hegde's deep-learning notes |
| `demo/q-learning.ipynb` | DQN, after [Curt-Park/rainbow-is-all-you-need](https://github.com/Curt-Park/rainbow-is-all-you-need) |
| `demo/ddpg_pendulum.ipynb` | the keras.io DDPG tutorial (amifunny, 2020) |
| `demo/Least_square_interpolation_Markowitz.ipynb` | LSPI over a B-spline basis for mean–variance allocation |

All four failed to import on the 2026 image: three depend on the retired `gym`
package, one on `bspline`. They have been ported to run headless, locally, with no
Colab and no display.

## The port

### Everything that touched `gym`

`gym` has been unmaintained since 2022; its successor is Farama's `gymnasium`,
which changes three things the notebooks relied on:

* `import gym` → `import gymnasium as gym`.
* `reset()` returns `(observation, info)`, not just the observation.
* `step()` returns `(obs, reward, terminated, truncated, info)` — the old single
  `done` flag is split into "the episode genuinely ended" and "the time limit ran
  out". Everywhere the notebooks used `done`, they now compute
  `done = terminated or truncated`, which reproduces the old semantics.
* Rendering is declared once, at construction: `gym.make(id, render_mode='rgb_array')`,
  after which `env.render()` returns an `(H, W, 3)` array. The old
  `env.render(mode='rgb_array')` raises.
* Environment ids were bumped: `Pendulum-v0` → `Pendulum-v1`,
  `LunarLander-v2` → `LunarLander-v3`, and the prose mention of
  `LunarLandingContinuous-v2` → `LunarLanderContinuous-v3`.

Links to `gymlibrary.dev` (the dead Gym docs) were repointed at
`gymnasium.farama.org`, and prose that said "OpenAI Gym" now says Gymnasium.

### Colab-only scaffolding, removed

* `rl-basics.ipynb`: the `!pip3 install imageio==2.4.1` / `!pip3 install gym[classic_control]`
  cell.
* `q-learning.ipynb`: the whole `IN_COLAB` bootstrap cell
  (`!apt install python-opengl ffmpeg xvfb`, `!pip install pyvirtualdisplay`,
  `!pip install gym`, `!pip install gym[box2d]`, `!apt autoremove`).

Nothing replaces them: the packages belong to the image (see below).

### Video rendering, replaced with something that works without a screen

* `rl-basics.ipynb` built a `moviepy` `ImageSequenceClip` and called
  `ipython_display(clip)`. That needs ffmpeg and a display. It now lays six evenly
  spaced `rgb_array` frames side by side with matplotlib, and writes the whole
  episode to `cartpole_trained.gif` with `imageio`.
* `q-learning.ipynb` looped `plt.imshow(frame); plt.show(); clear_output()` over
  every frame of the test episode — a thousand figures, an animation only in a live
  browser. Same treatment: a six-frame contact sheet plus `lunarlander_dqn.gif`.
* `ddpg_pendulum.ipynb` ended on two imgur GIFs recorded by the original author on a
  machine with a screen, and a third imgur screenshot standing in for the reward
  plot. The reward plot is produced by the notebook itself, so the screenshot is
  gone; the two GIFs are replaced by a real rollout of the trained actor through
  `render_mode='rgb_array'`, again a contact sheet plus `pendulum_ddpg.gif`.

The three GIFs and the four `pendulum_*.weights.h5` files are written into
`demo/` at run time and are not committed.

### Keras 3 / TF 2.21 (`ddpg_pendulum.ipynb`)

Independently of gym, this notebook was written against TF 2.x with the old
`tf.keras`, and needed work for Keras 3:

* `layers.Input(shape=(num_states))` → `shape=(num_states,)`. Keras 3 requires a
  tuple; an int is rejected.
* `save_weights("pendulum_actor.h5")` → `"pendulum_actor.weights.h5"`. Keras 3
  requires the `.weights.h5` suffix for weights-only saves.
* The replay buffer is allocated `float32` throughout. Keras 3 layers are float32
  and no longer quietly accept float64 input; `policy()` likewise returns a
  float32 action of shape `(1,)`, which is what `Pendulum-v1` expects.
* `update_target` used `set_weights()`, which under Keras 3 round-trips every
  weight through numpy on every environment step and dominated the runtime. It is
  now a single `@tf.function` (`update_targets`) that assigns into the target
  variables in place, reading the models from the enclosing scope — passing the
  variables in as arguments makes `tf.function` trace them into symbolic tensors,
  which have no `.assign`.
* The actor/critic gradient step was moved into a `@tf.function` as well. Eager,
  the demo took the better part of an hour on CPU; compiled, two minutes.

One trap worth recording, because it costs an hour to find: the models must be
called *without* `training=True`. The networks use `BatchNormalization`, and the
actor is called both on batches of 64 (in `update`) and on single states (in
`policy`). Both call sites have to agree, and the original relied on
inference-mode statistics. Setting `training=True` in `update` alone makes the
two disagree and the agent flatlines at about −1500 reward for all 100 episodes
while raising no error at all.

### Retuning

* `q-learning.ipynb` trained the DQN for 20 000 frames with a 1000-transition
  replay buffer. That is the upstream setting for CartPole; on Lunar Lander the
  lander never stops crashing (test score ≈ −110), which contradicts the
  notebook's own "Seems like we have done quite well!". Raised to 120 000 frames,
  `memory_size=50000`, `batch_size=64`, `target_update=200`,
  `epsilon_decay=1/40000`, and `plotting_interval=5000` so the progress plot does
  not redraw 600 times. The lander now lands (test score ≈ +120). A markdown line
  states the two-to-three-minute cost.
* `ddpg_pendulum.ipynb` keeps its 100 episodes but now pins the seed
  (`keras.utils.set_random_seed(1)` plus a one-off `env.reset(seed=42)`). DDPG on
  the Pendulum is strongly seed-dependent: of three seeds tried, two converged to
  about −170 average reward and one never left −1400. A demo whose story depends
  on the draw is not a demo. A markdown line says the seed is pinned and invites
  changing it.
* Nothing was reduced; no notebook came close to the five-minute budget.

### `Least_square_interpolation_Markowitz.ipynb`

No gym involvement. Two fixes:

* It needs `bspline` (`Bspline`, `splinelab`), which is not in the image. See below.
* `S = pd.DataFrame([], index=..., columns=...)` builds an *empty* frame, which in
  pandas 3 has dtype `object`; the object column survives the price simulation and
  reaches `scipy.interpolate.interp1d`, which raises
  `ValueError: object arrays are not supported`. Both such frames (`S` and
  `a_star`) are now allocated with `np.zeros(...)` so they are float from the
  start. This is the only change to the notebook's numerics, and the approximate
  optimal action still tracks the closed-form one.

### Housekeeping

Stored outputs were cleared from all four notebooks. What was in them was output
from the retired gym stack, and these are notebooks students execute themselves.

## Deletions and deduplication

None needed. The folder held exactly one copy of each of the four notebooks,
already under `demo/`; there were no stray copies at the lecture root or in a
nested `lecture_13/demo/`. Cells deleted inside notebooks are listed above.

## What the image must have

Already present on the 2026 image: `numpy` 2.5, `tensorflow` 2.21 / `keras` 3,
`torch` 2.14, `pandas`, `scipy`, `matplotlib`, `gymnasium` 1.3.

Must be added:

| package | needed by | why |
| --- | --- | --- |
| `gymnasium[classic-control]` (pulls `pygame`) | `rl-basics`, `ddpg_pendulum` | CartPole and Pendulum, and their `rgb_array` renderer |
| `gymnasium[box2d]` (pulls `box2d`, `swig`) | `q-learning` | `LunarLander-v3` |
| `imageio` | all three RL notebooks | writes the episode GIFs |
| `bspline` | `Least_square_interpolation_Markowitz` | `Bspline`, `splinelab` |

No longer needed, and should not be reinstated: `gym`, `moviepy`,
`pyvirtualdisplay`, `xvfb`, `python-opengl`. Nothing requires a display or a GPU.

## Verification

Executed from `content/lectures/lecture_13/demo/` with
`jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600`,
headless, CPU only, against a Python 3.12 environment mirroring the 2026 student
image.

| notebook | runtime | result |
| --- | --- | --- |
| `rl-basics.ipynb` | 11 s | 0 errors; reward threshold reached in 229 episodes, trained policy survives the full 500 steps |
| `q-learning.ipynb` | 167 s | 0 errors; test episode scores +120, i.e. the lander lands |
| `ddpg_pendulum.ipynb` | 123 s | 0 errors; average reward −1462 → −159 over 100 episodes |
| `Least_square_interpolation_Markowitz.ipynb` | 27 s | 0 errors; approximate optimal action ≈ −0.34 against the exact −0.26 |

Runtimes are wall-clock on an Apple-silicon CPU and will be somewhat higher on the
Nuvolos workspace; all four stay well inside the five-minute budget either way.
