# Almanac sketches

> Dormant candidate integrations for almanac; none is required by the current
> extraction or serving contract.

Topic: `almanac`

## YA-assisted acquisition

YA (yepanywhere, `~/ya`) can facilitate the user-assisted rungs by
offering to open the target URL in a YA-directed frame or new
tab/window — i.e. the user's *own* browser context, with their
session and vantage — then hand the rendered result back to the skill.
This plugs straight into the existing seam: the handed-back artifact
(serialized DOM, or a HAR) is exactly an `almanac update <name>
--source <file>` input, and a live YA-driven browser is the `remote`
rung's CDP target. No new engine contract is needed — YA would supply
acquisition, almanac keeps extraction/serving. Nothing here depends on
it; it is an ergonomics upgrade over hand-saving a page. Not yet
built; lives in the YA repo when it is.
