import * as vscode from 'vscode';
import OpenAI from 'openai';
import { GoogleGenerativeAI } from '@google/generative-ai';

let client: OpenAI | null = null;
let googleClient: GoogleGenerativeAI | null = null;
let currentProvider: string = 'openai';

function initializeClient() {
    const config = vscode.workspace.getConfiguration('spect-armykit');
    const provider = config.get<string>('apiProvider', 'openai');
    currentProvider = provider;
    const model = config.get<string>('model', 'gpt-4o-mini');

    switch (provider) {
        case 'openai':
            const openaiKey = config.get<string>('openai.apiKey');
            const openaiBaseURL = config.get<string>('openai.baseURL', 'https://api.openai.com/v1');
            if (openaiKey) {
                client = new OpenAI({ apiKey: openaiKey, baseURL: openaiBaseURL });
            }
            break;
        case 'azure':
            const azureEndpoint = config.get<string>('azure.endpoint');
            const azureKey = config.get<string>('azure.apiKey');
            const azureModel = config.get<string>('azure.model', 'gpt-4');
            if (azureEndpoint && azureKey) {
                client = new OpenAI({
                    baseURL: azureEndpoint,
                    apiKey: azureKey,
                    defaultHeaders: { 'api-version': '2024-02-01' }
                });
            }
            break;
        case 'github':
            const githubEndpoint = config.get<string>('github.endpoint', 'https://models.inference.ai.azure.com');
            const githubKey = config.get<string>('github.apiKey');
            if (githubKey) {
                client = new OpenAI({
                    baseURL: githubEndpoint,
                    apiKey: githubKey,
                    defaultHeaders: { 'api-version': '2024-02-01' }
                });
            }
            break;
        case 'google':
            const googleKey = config.get<string>('google.apiKey');
            if (googleKey) {
                googleClient = new GoogleGenerativeAI(googleKey);
            }
            break;
        case 'deepseek':
            const deepseekKey = config.get<string>('deepseek.apiKey');
            const deepseekBaseURL = config.get<string>('deepseek.baseURL', 'https://api.deepseek.com/v1');
            if (deepseekKey) {
                client = new OpenAI({ apiKey: deepseekKey, baseURL: deepseekBaseURL });
            }
            break;
        case 'sherpa':
            const sherpaKey = config.get<string>('sherpa.apiKey');
            const sherpaBaseURL = config.get<string>('sherpa.baseURL', 'https://api.sherpacoder.com/v1');
            if (sherpaKey) {
                client = new OpenAI({ apiKey: sherpaKey, baseURL: sherpaBaseURL });
            }
            break;
        case 'local':
        case 'gpt4all':
        case 'ollama':
            const localEndpoint = provider === 'local' ? config.get<string>('local.endpoint', 'http://localhost:11434/v1') :
                                 provider === 'gpt4all' ? config.get<string>('gpt4all.endpoint', 'http://localhost:4891/v1') :
                                 'http://localhost:11434/v1'; // ollama default
            client = new OpenAI({ baseURL: localEndpoint, apiKey: 'not-needed' });
            break;
    }
}

class NotebookMemory {
    logs: any[] = [];

    log(agent: string, action: string, result: any) {
        const entry = { agent, action, result, timestamp: new Date().toISOString() };
        this.logs.push(entry);
        console.log(`Logged: ${JSON.stringify(entry)}`);
    }

    getHistory() {
        return this.logs;
    }
}

const notebook = new NotebookMemory();

class BaseAgent {
    name: string;
    role: string;
    active: boolean = true;

    constructor(name: string, role: string) {
        this.name = name;
        this.role = role;
    }

    async think(prompt: string): Promise<string> {
        const config = vscode.workspace.getConfiguration('spect-armykit');
        // Determine model based on provider
        let modelName: string;
        switch (currentProvider) {
            case 'deepseek':
                modelName = config.get<string>('deepseek.model', 'deepseek-coder')!;
                break;
            case 'sherpa':
                modelName = config.get<string>('sherpa.model', 'sherpa-coder')!;
                break;
            default:
                modelName = config.get<string>('model', 'gpt-4o-mini')!;
        }
        if (currentProvider === 'google') {
            if (!googleClient) return "Google AI client not configured";
            try {
                console.log('Thinking with Google, prompt:', prompt);
                const model = googleClient.getGenerativeModel({ model: modelName });
                const fullPrompt = `You are ${this.name}, a ${this.role}. ${prompt}`;
                const result = await model.generateContent(fullPrompt);
                const response = await result.response;
                const text = response.text();
                console.log('Google response:', text);
                notebook.log(this.name, "think", text);
                return text;
            } catch (error) {
                console.log('Google error:', error);
                return `Error: ${error}`;
            }
        } else {
            if (!client) return "No AI client configured";
            try {
                const response = await client.chat.completions.create({
                    messages: [
                        { role: 'system', content: `You are ${this.name}, a ${this.role}.` },
                        { role: 'user', content: prompt }
                    ],
                    model: modelName
                });
                const result = response.choices[0].message.content || "";
                notebook.log(this.name, "think", result);
                return result;
            } catch (error) {
                return `Error: ${error}`;
            }
        }
    }

    dissolve() {
        this.active = false;
        notebook.log(this.name, "dissolve", "Agent dissolved");
    }
}

class MasterAssistantAI extends BaseAgent {
    constructor() {
        super("MasterAssistantAI", "Human Interface Agent");
    }

    async interpretInput(userInput: string): Promise<string> {
        return await this.think(`Interpret this user request and create a clear spec: ${userInput}`);
    }

    confirmSpec(spec: string): boolean {
        vscode.window.showInformationMessage(`Interpreted spec: ${spec}`);
        return true; // Assume confirmed
    }
}

class MasterAgent extends BaseAgent {
    constructor() {
        super("MasterAgent", "Orchestrator Agent");
    }

    async validateSpec(spec: string): Promise<boolean> {
        const validation = await this.think(`Validate this spec for structure and feasibility: ${spec}`);
        return validation.toLowerCase().includes("valid");
    }

    routeToManager(spec: string): string {
        return spec;
    }
}

class ManagerAgent extends BaseAgent {
    constructor() {
        super("ManagerAgent", "Task Breakdown Agent");
    }

    async breakIntoModules(spec: string): Promise<any[]> {
        const modulesStr = await this.think(`Break this spec into modules (UI, backend, auth, DB, etc.): ${spec}`);
        // Placeholder parsing
        return [{ name: "UI", description: "User interface" }, { name: "Backend", description: "Server logic" }];
    }
}

class SubmanagerAgent extends BaseAgent {
    constructor(domain: string) {
        super(`Submanager-${domain}`, `${domain} Submanager`);
    }

    spawnTeamLeader(module: any): TeamLeaderAgent {
        return new TeamLeaderAgent(module.name);
    }
}

class TeamLeaderAgent extends BaseAgent {
    constructor(moduleName: string) {
        super(`TeamLeader-${moduleName}`, `Team Leader for ${moduleName}`);
    }

    spawnMiniArmy(feature: string): MiniAIArmy {
        return new MiniAIArmy(feature);
    }
}

class MiniAIArmy extends BaseAgent {
    constructor(feature: string) {
        super(`MiniArmy-${feature}`, `Mini AI Army for ${feature}`);
    }

    async executeFeature(): Promise<string> {
        return await this.think(`Generate code and logic for feature: ${this.name.split('-')[1]}`);
    }
}

export function activate(context: vscode.ExtensionContext) {
    console.log('Spect Sun Armies Kit extension activated');
    initializeClient();

    const chatParticipant = vscode.chat.createChatParticipant('spect-armykit.chat', async (request, context, response, token) => {
        console.log('Chat request received:', request.prompt);
        initializeClient(); // Re-init in case settings changed
        if (currentProvider === 'google' && !googleClient) {
            response.markdown('Google AI client not configured. Please set Google API key in VS Code Settings > Spect Sun Armies Kit.');
            return;
        } else if (!client) {
            response.markdown('AI client not configured. Please set API provider and keys in VS Code Settings > Spect Sun Armies Kit.');
            return;
        }

        const userInput = request.prompt;
        try {
            const assistant = new MasterAssistantAI();
            const spec = await assistant.interpretInput(userInput);
            response.markdown(`**Interpreted Spec:** ${spec}\n\nProcessing through agent hierarchy...`);
            const master = new MasterAgent();
            if (await master.validateSpec(spec)) {
                response.markdown('Spec validated. Breaking into modules...');
                const manager = new ManagerAgent();
                const modules = await manager.breakIntoModules(spec);
                for (const module of modules) {
                    response.markdown(`Processing module: ${module.name} - ${module.description}`);
                    const submanager = new SubmanagerAgent(module.name);
                    const teamLeader = submanager.spawnTeamLeader(module);
                    const miniArmy = teamLeader.spawnMiniArmy(module.description);
                    const result = await miniArmy.executeFeature();
                    response.markdown(`**Result for ${module.name}:** ${result}`);
                    miniArmy.dissolve();
                    teamLeader.dissolve();
                    submanager.dissolve();
                }
                manager.dissolve();
                response.markdown('All modules processed. Agent hierarchy dissolved.');
            } else {
                response.markdown('Spec validation failed.');
            }
            master.dissolve();
            assistant.dissolve();
        } catch (error) {
            response.markdown(`Error: ${error}`);
        }
    });

    const openIdeCommand = vscode.commands.registerCommand('spect-armykit.openIde', async () => {
        if (!client) {
            vscode.window.showErrorMessage('AI client not configured. Please check your Spect Sun Armies Kit settings.');
            return;
        }
        const userInput = await vscode.window.showInputBox({ prompt: 'Enter your request for the AI IDE' });
        if (!userInput) return;

        const assistant = new MasterAssistantAI();
        const spec = await assistant.interpretInput(userInput);
        if (assistant.confirmSpec(spec)) {
            const master = new MasterAgent();
            if (await master.validateSpec(spec)) {
                const manager = new ManagerAgent();
                const modules = await manager.breakIntoModules(spec);
                for (const module of modules) {
                    const submanager = new SubmanagerAgent(module.name);
                    const teamLeader = submanager.spawnTeamLeader(module);
                    const miniArmy = teamLeader.spawnMiniArmy(module.description);
                    const result = await miniArmy.executeFeature();
                    vscode.window.showInformationMessage(`Feature result: ${result}`);
                    miniArmy.dissolve();
                    teamLeader.dissolve();
                    submanager.dissolve();
                }
                manager.dissolve();
            }
            master.dissolve();
        }
        assistant.dissolve();
    });

    const selectModelCommand = vscode.commands.registerCommand('spect-armykit.selectModel', async () => {
        if (!client && !googleClient) {
            vscode.window.showErrorMessage('AI client not configured. Initialize a provider first.');
            return;
        }
        const config = vscode.workspace.getConfiguration('spect-armykit');
        let modelList: string[] = [];
        try {
            switch (currentProvider) {
                case 'openai':
                case 'azure':
                case 'github':
                    // Predefined free or common models
                    modelList = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4', 'gpt-4-32k', 'gpt-4o-mini'];
                    break;
                case 'deepseek':
                    modelList = [config.get<string>('deepseek.model', 'deepseek-coder')!];
                    break;
                case 'sherpa':
                    modelList = [config.get<string>('sherpa.model', 'sherpa-coder')!];
                    break;
                case 'local':
                case 'gpt4all':
                case 'ollama':
                    // Attempt to list models, fallback to configured default
                    if (client) {
                        try {
                            const response = await client.models.list();
                            modelList = response.data.map((m: any) => m.id);
                        } catch {
                            modelList = [config.get<string>('model', 'gpt-4o-mini')!];
                        }
                    } else {
                        modelList = [config.get<string>('model', 'gpt-4o-mini')!];
                    }
                    break;
                default:
                    modelList = [config.get<string>('model', 'gpt-4o-mini')!];
            }
        } catch (err) {
            vscode.window.showErrorMessage(`Error fetching models: ${err}`);
            return;
        }
        if (modelList.length === 0) {
            vscode.window.showInformationMessage('No models found.');
            return;
        }
        const choice = await vscode.window.showQuickPick(modelList, { placeHolder: 'Select AI model' });
        if (choice) {
            const config = vscode.workspace.getConfiguration('spect-armykit');
            // Determine config key to update
            let settingKey = 'model';
            if (currentProvider === 'deepseek') settingKey = 'deepseek.model';
            else if (currentProvider === 'sherpa') settingKey = 'sherpa.model';
            await config.update(settingKey, choice, vscode.ConfigurationTarget.Global);
            vscode.window.showInformationMessage(`Model set to ${choice}`);
        }
    });

    context.subscriptions.push(chatParticipant);
    context.subscriptions.push(openIdeCommand);
    context.subscriptions.push(selectModelCommand);
}

export function deactivate() {}