import { FormEvent, useState } from "react";
import type { SearchPayload } from "../lib/api";

type Props = {
  onSubmit: (payload: SearchPayload) => Promise<void>;
  loading: boolean;
};

export function SearchForm({ onSubmit, loading }: Props) {
  const [payload, setPayload] = useState<SearchPayload>({
    username: "",
    platform: "",
    email: "",
    phone: "",
    full_name: "",
    photo_url: "",
    consent_confirmed: false,
  });

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    await onSubmit(payload);
  };

  return (
    <form className="panel" onSubmit={submit}>
      <h2>Input Signals</h2>
      <p className="muted">Provide one or more public identifiers. Consent is required.</p>

      <div className="grid">
        <label>
          Username
          <input value={payload.username} onChange={(e) => setPayload({ ...payload, username: e.target.value })} />
        </label>

        <label>
          Platform
          <select value={payload.platform} onChange={(e) => setPayload({ ...payload, platform: e.target.value })}>
            <option value="">Any</option>
            <option value="github">GitHub</option>
            <option value="x">X</option>
            <option value="instagram">Instagram</option>
            <option value="linkedin">LinkedIn</option>
          </select>
        </label>

        <label>
          Email
          <input type="email" value={payload.email} onChange={(e) => setPayload({ ...payload, email: e.target.value })} />
        </label>

        <label>
          Phone (E.164)
          <input value={payload.phone} onChange={(e) => setPayload({ ...payload, phone: e.target.value })} />
        </label>

        <label>
          Full Name
          <input value={payload.full_name} onChange={(e) => setPayload({ ...payload, full_name: e.target.value })} />
        </label>

        <label>
          Photo URL
          <input type="url" value={payload.photo_url} onChange={(e) => setPayload({ ...payload, photo_url: e.target.value })} />
        </label>
      </div>

      <label className="consent">
        <input
          type="checkbox"
          checked={payload.consent_confirmed}
          onChange={(e) => setPayload({ ...payload, consent_confirmed: e.target.checked })}
        />
        I confirm lawful purpose and documented consent.
      </label>

      <button disabled={loading}>{loading ? "Searching..." : "Run Reverse Search"}</button>
    </form>
  );
}
