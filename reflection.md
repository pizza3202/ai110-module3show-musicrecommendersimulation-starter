# Profile comparison reflections

Plain-language notes comparing pairs of stress-test profiles from `src/main.py`. Each pair highlights how the same small catalog can produce **different** top lists because the scoring recipe only “sees” tags and numbers, not real sound.

---

### High-Energy Pop ↔ Chill Lofi

**High-Energy Pop** asks for loud, happy, produced pop, so the system hunts rows where the words **pop** and **happy** appear together and the energy number sits near your target. **Chill Lofi** asks for quiet, relaxed lofi with acoustic lean, so the winners are completely different rows: soft **lofi** + **chill** tracks with high acousticness scores. Nothing is “wrong” here—the lists differ because the *instructions* differ, like asking a DJ for a party set versus a study playlist.

---

### High-Energy Pop ↔ Deep Intense Rock

Both profiles want **high energy**, but one locks onto **pop** and **happy** while the other locks onto **rock** and **intense**. The recommender is strict about those words, so **Sunrise City** leads the pop list while **Storm Runner** leads the rock list even though both songs are “loud.” If the same song appeared first for both, we would worry the model was ignoring genre; instead it shows the **genre gate** working.

---

### High-Energy Pop ↔ Edge case (pop + moody + very high energy)

Here is the **Gym Hero** effect in words. The edge profile says **moody**, but almost no song in the table is tagged **pop** and **moody** at the same time. The program still has to pick something, so it grabs a **pop** song with **intense** energy that lines up almost perfectly with the **energy number** you typed—even though “intense gym pop” is not the same feeling as “moody.” To a non-programmer: imagine you asked a friend for “sad upbeat pop” and they only own party tracks; they hand you the **closest word match** they have, not mind-reading.

---

### Chill Lofi ↔ Deep Intense Rock

**Chill Lofi** rewards low energy and acoustic texture inside the lofi/chill corner of the file. **Deep Intense Rock** rewards rock, intense mood, and very high energy—almost the opposite corner of the spreadsheet. Top titles barely overlap because the model is not trying to balance your life; it is **maximizing points** for each separate wish list.

---

### Chill Lofi ↔ Edge case

The lofi profile wants **gentle** numbers and **acoustic** credit. The edge profile wants **explosive** energy under **pop** and never finds a moody mood match. So the lofi run feels “cozy and consistent,” while the edge run looks more like a **loud pop** sampler with broken mood promises. Same recommender code—different **holes** in the data for what the user claimed.

---

### Deep Intense Rock ↔ Edge case

Both want **very high energy**, so you might expect similar songs. In practice the **rock** profile still insists on the word **rock**, which filters down to metal and rock rows, while the **pop** edge profile stays inside pop—even when mood does not match—because the **+2 genre** bonus is huge. That is why **Storm Runner** can top one list and **Gym Hero** another: the **first gate is the genre string**, not “how loud it feels in the room.”

---

### Weight experiment (same High-Energy Pop, different weights)

Not a “pair of people,” but a pair of **runs**: baseline weights versus **double energy / half genre**. Number one stayed **Sunrise City**, but lower slots swapped toward tracks whose **energy digit** matched the target more tightly. In everyday language: when we told the formula to care **more** about the energy dial, it acted like someone who turns the volume knob before asking whether the song is still the right *style* for the room.
