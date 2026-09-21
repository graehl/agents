import assert from "node:assert/strict";
import test from "node:test";
import { notes, filterNotes } from "../notes.ts";

test("search combines words and category, preserves content and handles empty results", () => {
  assert.equal(filterNotes(notes, "", "all").length, 3);
  assert.deepEqual(filterNotes(notes, "  SMALL   BEGINNING ", "make"), [notes[0]]);
  assert.equal(filterNotes(notes, "small", "explore").length, 0);
  assert.equal(filterNotes(notes, "not-present", "all").length, 0);
  assert.equal(filterNotes(notes, "", "make").length, 2);
  assert.equal(notes.length, 3);
});
