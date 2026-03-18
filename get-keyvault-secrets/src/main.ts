import * as core from "@actions/core";
import { execFileSync } from "child_process";

const MAX_RETRY_ATTEMPTS = 3;
const RETRY_DELAY_MS = 3000;

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getSecret(keyvault: string, secretName: string): Promise<string> {
  for (let attempt = 1; attempt <= MAX_RETRY_ATTEMPTS; attempt++) {
    try {
      return execFileSync(
        "az",
        [
          "keyvault",
          "secret",
          "show",
          "--vault-name",
          keyvault,
          "--name",
          secretName,
          "--query",
          "value",
          "-o",
          "tsv",
        ],
        { encoding: "utf8", stdio: ["pipe", "pipe", "pipe"] },
      ).trim();
    } catch (error) {
      if (attempt === MAX_RETRY_ATTEMPTS) {
        throw error;
      }
      core.debug(
        `Attempt ${attempt} failed for secret "${secretName}", retrying in ${RETRY_DELAY_MS}ms...`,
      );
      await sleep(RETRY_DELAY_MS);
    }
  }
}

async function run(): Promise<void> {
  try {
    const keyvault = core.getInput("keyvault", { required: true });
    const secretsInput = core.getInput("secrets", { required: true });
    const secretNames = secretsInput
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    for (const secretName of secretNames) {
      const value = await getSecret(keyvault, secretName);
      core.setSecret(value);
      core.setOutput(secretName, value);
    }
  } catch (error) {
    core.setFailed(error instanceof Error ? error.message : String(error));
  }
}

run();
